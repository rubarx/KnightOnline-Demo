#!/usr/bin/env python3
"""
Knight Online .UIF File Tool
Creates and edits UI files for Knight Online client.

Format order (as per N3UIBase::Save/Load):
1. Children count (int16 + int16 reserved for v1264+, int32 for older)
2. For each child (in reverse order for save):
   a. UI type (int32)
   b. Child element (recursively: base + specific)
3. Base properties (ID, Region, Style, Tooltip, Sounds)
4. Element-specific data (Image: texture+UV, Button: click rect+sounds, String: font+text)

Author: Claude AI
Date: 2026-01-28
"""

import struct
import os
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import IntEnum


class UIType(IntEnum):
    """UI Element types as defined in the Knight Online engine"""
    UI_TYPE_BASE = 0
    UI_TYPE_IMAGE = 1
    UI_TYPE_STRING = 2
    UI_TYPE_BUTTON = 3
    UI_TYPE_STATIC = 4
    UI_TYPE_PROGRESS = 5
    UI_TYPE_SCROLLBAR = 6
    UI_TYPE_TRACKBAR = 7
    UI_TYPE_EDIT = 8
    UI_TYPE_AREA = 9
    UI_TYPE_LIST = 10
    UI_TYPE_TOOLTIP = 11
    UI_TYPE_ICONSLOT = 12


class ButtonState(IntEnum):
    """Button state images stored in m_dwReserved"""
    BS_NORMAL = 0
    BS_DOWN = 1
    BS_ON = 2
    BS_DISABLE = 3


@dataclass
class Rect:
    """Rectangle structure"""
    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0

    def pack(self) -> bytes:
        return struct.pack('<iiii', self.left, self.top, self.right, self.bottom)

    @classmethod
    def unpack(cls, data: bytes) -> 'Rect':
        left, top, right, bottom = struct.unpack('<iiii', data[:16])
        return cls(left, top, right, bottom)

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top


@dataclass
class UIElement:
    """Base UI element"""
    ui_type: UIType = UIType.UI_TYPE_BASE
    name: str = ""  # m_szName from CN3BaseFileAccess (internal resource name)
    element_id: str = ""  # m_szID (UI element ID for lookup)
    region: Rect = field(default_factory=Rect)
    movable_region: Rect = field(default_factory=Rect)
    style: int = 0
    reserved: int = 0
    tooltip: str = ""
    sound_open: str = ""
    sound_close: str = ""
    children: List['UIElement'] = field(default_factory=list)

    def pack_string(self, s: str) -> bytes:
        """Pack a length-prefixed string"""
        if not s:
            return struct.pack('<i', 0)
        encoded = s.encode('utf-8')
        return struct.pack('<i', len(encoded)) + encoded

    def pack_base(self) -> bytes:
        """Pack base element properties (ID, Region, Style, Tooltip, Sounds)"""
        data = b''
        data += self.pack_string(self.element_id)
        data += self.region.pack()
        data += self.movable_region.pack()
        data += struct.pack('<I', self.style)
        data += struct.pack('<I', self.reserved)
        data += self.pack_string(self.tooltip)
        data += self.pack_string(self.sound_open)
        data += self.pack_string(self.sound_close)
        return data

    def pack_specific(self) -> bytes:
        """Pack element-specific data (override in subclasses)"""
        return b''

    def pack(self, version: int = 1298) -> bytes:
        """Pack the entire element including children

        Order (as per CN3BaseFileAccess::Save + CN3UIBase::Save):
        1. m_szName (from CN3BaseFileAccess)
        2. Children count
        3. Children (type + recursive pack) - in REVERSE order
        4. Base properties (m_szID, Region, Style, etc.)
        5. Element-specific data
        """
        data = b''

        # 1. m_szName (CN3BaseFileAccess format)
        data += self.pack_string(self.name)

        # 2. Children count (version 1264+ uses int16 + int16)
        if version >= 1264:
            data += struct.pack('<hh', len(self.children), 1)
        else:
            data += struct.pack('<i', len(self.children))

        # 3. Pack children in REVERSE order (as per engine)
        for child in reversed(self.children):
            data += struct.pack('<i', child.ui_type)
            data += child.pack(version)

        # 4. Base properties
        data += self.pack_base()

        # 5. Element-specific data (for subclasses)
        data += self.pack_specific()

        return data


@dataclass
class UIImage(UIElement):
    """Image UI element"""
    texture_path: str = ""
    uv_left: float = 0.0
    uv_top: float = 0.0
    uv_right: float = 1.0
    uv_bottom: float = 1.0
    anim_frame_rate: float = 30.0

    def __post_init__(self):
        self.ui_type = UIType.UI_TYPE_IMAGE

    def pack_specific(self) -> bytes:
        """Pack image-specific data (comes AFTER base properties)"""
        data = b''
        data += self.pack_string(self.texture_path)
        data += struct.pack('<ffff', self.uv_left, self.uv_top, self.uv_right, self.uv_bottom)
        data += struct.pack('<f', self.anim_frame_rate)
        return data


@dataclass
class UIString(UIElement):
    """String/Text UI element"""
    font_name: str = "Arial"
    font_height: int = 12
    font_flags: int = 0  # 1=bold, 2=italic
    color: int = 0xFFFFFFFF  # ARGB
    text: str = ""
    line_spacing: int = 0

    def __post_init__(self):
        self.ui_type = UIType.UI_TYPE_STRING

    def pack_specific(self) -> bytes:
        """Pack string-specific data"""
        data = b''
        data += self.pack_string(self.font_name)
        data += struct.pack('<I', self.font_height)
        data += struct.pack('<I', self.font_flags)
        data += struct.pack('<I', self.color)
        data += self.pack_string(self.text)
        data += struct.pack('<i', self.line_spacing)
        return data


@dataclass
class UIButton(UIElement):
    """Button UI element"""
    click_rect: Rect = field(default_factory=Rect)
    sound_on: str = ""
    sound_click: str = ""

    def __post_init__(self):
        self.ui_type = UIType.UI_TYPE_BUTTON

    def pack_specific(self) -> bytes:
        """Pack button-specific data"""
        data = b''
        data += self.click_rect.pack()
        data += self.pack_string(self.sound_on)
        data += self.pack_string(self.sound_click)
        return data

    def add_state_image(self, state: ButtonState, texture: str, uv: tuple, region: Rect):
        """Add a button state image"""
        img = UIImage(
            element_id=f"img_state_{state}",
            texture_path=texture,
            uv_left=uv[0],
            uv_top=uv[1],
            uv_right=uv[2],
            uv_bottom=uv[3],
            region=region,
            reserved=state  # Button state stored in reserved
        )
        self.children.append(img)


@dataclass
class UIStatic(UIElement):
    """Static text/button UI element"""
    sound_click: str = ""

    def __post_init__(self):
        self.ui_type = UIType.UI_TYPE_STATIC

    def pack_specific(self) -> bytes:
        """Pack static-specific data"""
        data = b''
        data += self.pack_string(self.sound_click)
        return data


class UIFile:
    """Knight Online .UIF file handler"""

    def __init__(self, version: int = 1298):
        self.version = version
        self.root: Optional[UIElement] = None

    def save(self, filepath: str):
        """Save the UI file"""
        if self.root is None:
            raise ValueError("No root element defined")

        with open(filepath, 'wb') as f:
            # Root element pack includes m_szName at the beginning
            f.write(self.root.pack(self.version))

    @staticmethod
    def read_string(f) -> str:
        """Read a length-prefixed string"""
        length_data = f.read(4)
        if len(length_data) < 4:
            return ""
        length = struct.unpack('<i', length_data)[0]
        if length > 0 and length < 8192:
            data = f.read(length)
            return data.decode('utf-8', errors='replace')
        return ""

    def load(self, filepath: str) -> UIElement:
        """Load a UI file"""
        with open(filepath, 'rb') as f:
            # Read root element (as UI_TYPE_BASE)
            # _read_element now reads m_szName first
            self.root = self._read_element(f, UIType.UI_TYPE_BASE)

        return self.root

    def _read_element(self, f, ui_type: UIType) -> UIElement:
        """Read a UI element recursively"""
        # Create element based on type
        if ui_type == UIType.UI_TYPE_IMAGE:
            elem = UIImage()
        elif ui_type == UIType.UI_TYPE_STRING:
            elem = UIString()
        elif ui_type == UIType.UI_TYPE_BUTTON:
            elem = UIButton()
        elif ui_type == UIType.UI_TYPE_STATIC:
            elem = UIStatic()
        else:
            elem = UIElement()
        elem.ui_type = ui_type

        # 1. Read m_szName (from CN3BaseFileAccess)
        elem.name = self.read_string(f)

        # 2. Read children count
        if self.version >= 1264:
            child_count_data = f.read(4)
            if len(child_count_data) < 4:
                child_count = 0
            else:
                child_count = struct.unpack('<h', child_count_data[:2])[0]
                # Skip 2 bytes reserved
        else:
            child_count_data = f.read(4)
            if len(child_count_data) < 4:
                child_count = 0
            else:
                child_count = struct.unpack('<i', child_count_data)[0]

        # Read children (in reverse order - first read goes to end)
        children = []
        for _ in range(max(0, min(child_count, 100))):  # Limit to 100 children max
            type_data = f.read(4)
            if len(type_data) < 4:
                break
            child_type_val = struct.unpack('<i', type_data)[0]
            if child_type_val < 0 or child_type_val > 12:
                break
            child_type = UIType(child_type_val)
            child = self._read_element(f, child_type)
            children.insert(0, child)  # Insert at front to reverse
        elem.children = children

        # Read base properties
        elem.element_id = self.read_string(f)

        region_data = f.read(16)
        if len(region_data) >= 16:
            elem.region = Rect.unpack(region_data)

        movable_data = f.read(16)
        if len(movable_data) >= 16:
            elem.movable_region = Rect.unpack(movable_data)

        style_data = f.read(4)
        if len(style_data) >= 4:
            elem.style = struct.unpack('<I', style_data)[0]

        reserved_data = f.read(4)
        if len(reserved_data) >= 4:
            elem.reserved = struct.unpack('<I', reserved_data)[0]

        elem.tooltip = self.read_string(f)
        elem.sound_open = self.read_string(f)
        elem.sound_close = self.read_string(f)

        # Read element-specific data
        if ui_type == UIType.UI_TYPE_IMAGE:
            elem.texture_path = self.read_string(f)
            uv_data = f.read(16)
            if len(uv_data) >= 16:
                elem.uv_left, elem.uv_top, elem.uv_right, elem.uv_bottom = struct.unpack('<ffff', uv_data)
            anim_data = f.read(4)
            if len(anim_data) >= 4:
                elem.anim_frame_rate = struct.unpack('<f', anim_data)[0]

        elif ui_type == UIType.UI_TYPE_STRING:
            elem.font_name = self.read_string(f)
            height_data = f.read(4)
            if len(height_data) >= 4:
                elem.font_height = struct.unpack('<I', height_data)[0]
            flags_data = f.read(4)
            if len(flags_data) >= 4:
                elem.font_flags = struct.unpack('<I', flags_data)[0]
            color_data = f.read(4)
            if len(color_data) >= 4:
                elem.color = struct.unpack('<I', color_data)[0]
            elem.text = self.read_string(f)
            spacing_data = f.read(4)
            if len(spacing_data) >= 4:
                elem.line_spacing = struct.unpack('<i', spacing_data)[0]

        elif ui_type == UIType.UI_TYPE_BUTTON:
            click_data = f.read(16)
            if len(click_data) >= 16:
                elem.click_rect = Rect.unpack(click_data)
            elem.sound_on = self.read_string(f)
            elem.sound_click = self.read_string(f)

        elif ui_type == UIType.UI_TYPE_STATIC:
            elem.sound_click = self.read_string(f)

        return elem


def create_town_buttons_ui() -> UIFile:
    """
    Create the co_townbuttons_us.uif file for town teleport.
    Simple single button that triggers /town command.
    """
    uif = UIFile(version=1298)

    # Small button dimensions
    button_width = 60
    button_height = 24

    # Position near bottom-right of screen (like modern KO clients)
    # Screen is typically 1024x768, place button at bottom right area
    button_x = 900
    button_y = 700

    # Create root element (just the button, no window frame)
    root = UIButton(
        element_id="Btn_Town",
        region=Rect(button_x, button_y, button_x + button_width, button_y + button_height),
        click_rect=Rect(button_x, button_y, button_x + button_width, button_y + button_height),
        tooltip="Teleport to town (/town)"
    )

    # Button normal state image
    btn_bg = UIImage(
        element_id="Btn_Town_bg",
        texture_path="ui_us\\ui_warfare_us.dxt",
        region=Rect(button_x, button_y, button_x + button_width, button_y + button_height),
        uv_left=0.4,
        uv_top=0.0,
        uv_right=0.459,
        uv_bottom=0.0234375,
        reserved=ButtonState.BS_NORMAL
    )
    root.children.append(btn_bg)

    # Button pressed state
    btn_down = UIImage(
        element_id="Btn_Town_down",
        texture_path="ui_us\\ui_warfare_us.dxt",
        region=Rect(button_x, button_y, button_x + button_width, button_y + button_height),
        uv_left=0.4,
        uv_top=0.025,
        uv_right=0.459,
        uv_bottom=0.0484375,
        reserved=ButtonState.BS_DOWN
    )
    root.children.append(btn_down)

    # Button label
    label = UIString(
        element_id="Btn_Town_text",
        text="Town",
        region=Rect(button_x + 5, button_y + 5, button_x + button_width - 5, button_y + 19),
        font_name="Arial",
        font_height=11,
        font_flags=1,  # Bold
        color=0xFFFFFFFF,
        style=0x00000002  # UISTYLE_STRING_ALIGNCENTER
    )
    root.children.append(label)

    uif.root = root
    return uif


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Knight Online .UIF File Tool")
    parser.add_argument('--create-town-buttons', action='store_true',
                        help='Create co_townbuttons_us.uif')
    parser.add_argument('--output', '-o', type=str, default='.',
                        help='Output directory')
    parser.add_argument('--read', '-r', type=str,
                        help='Read and dump a .uif file')

    args = parser.parse_args()

    if args.read:
        print(f"Reading {args.read}...")
        uif = UIFile()
        try:
            root = uif.load(args.read)
            print_element(root, 0)
        except Exception as e:
            print(f"Error reading file: {e}")
            import traceback
            traceback.print_exc()

    if args.create_town_buttons:
        output_path = os.path.join(args.output, "co_townbuttons_us.uif")
        print(f"Creating {output_path}...")
        uif = create_town_buttons_ui()
        uif.save(output_path)
        print(f"Created {output_path}")
        print(f"File size: {os.path.getsize(output_path)} bytes")


def print_element(elem: UIElement, indent: int = 0):
    """Print element hierarchy for debugging"""
    prefix = "  " * indent
    name_str = f" name='{elem.name}'" if elem.name else ""
    id_str = f" id='{elem.element_id}'" if elem.element_id else ""
    print(f"{prefix}[{elem.ui_type.name}]{name_str}{id_str}")
    print(f"{prefix}  Region: ({elem.region.left}, {elem.region.top}, {elem.region.right}, {elem.region.bottom})")
    print(f"{prefix}  Style: 0x{elem.style:08X}, Reserved: {elem.reserved}")

    if isinstance(elem, UIImage):
        print(f"{prefix}  Texture: {elem.texture_path}")
        print(f"{prefix}  UV: ({elem.uv_left:.4f}, {elem.uv_top:.4f}, {elem.uv_right:.4f}, {elem.uv_bottom:.4f})")

    elif isinstance(elem, UIString):
        print(f"{prefix}  Font: {elem.font_name} {elem.font_height}px flags={elem.font_flags}")
        print(f"{prefix}  Color: 0x{elem.color:08X}")
        print(f"{prefix}  Text: \"{elem.text}\"")

    elif isinstance(elem, UIButton):
        print(f"{prefix}  Click Rect: ({elem.click_rect.left}, {elem.click_rect.top}, {elem.click_rect.right}, {elem.click_rect.bottom})")
        if elem.sound_on:
            print(f"{prefix}  Sound On: {elem.sound_on}")
        if elem.sound_click:
            print(f"{prefix}  Sound Click: {elem.sound_click}")

    if elem.tooltip:
        print(f"{prefix}  Tooltip: \"{elem.tooltip}\"")

    for child in elem.children:
        print_element(child, indent + 1)


if __name__ == "__main__":
    main()
