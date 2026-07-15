import os

xml_header = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Material 3 Components Gallery</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QLabel" name="titleLabel">
      <property name="text">
       <string>Buttons</string>
      </property>
      <property name="alignment">
       <set>Qt::AlignCenter</set>
      </property>
      <property name="class" stdset="0">
       <string>displayMedium</string>
      </property>
     </widget>
    </item>
    <item>
     <layout class="QGridLayout" name="gridLayout">
"""

xml_footer = """     </layout>
    </item>
    <item>
     <spacer name="verticalSpacer">
      <property name="orientation">
       <enum>Qt::Vertical</enum>
      </property>
      <property name="sizeHint" stdset="0">
       <size>
        <width>20</width>
        <height>40</height>
       </size>
      </property>
     </spacer>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


def make_label(text, row, col):
    """Genera el XML para una etiqueta."""
    return f"""      <item row="{row}" column="{col}">
       <widget class="QLabel" name="lbl_{row}_{col}">
        <property name="text">
         <string>{text}</string>
        </property>
        <property name="alignment">
         <set>Qt::AlignCenter</set>
        </property>
        <property name="class" stdset="0">
         <string>labelLarge</string>
        </property>
       </widget>
      </item>
"""


def make_btn(btn_type, row, col, has_icon=False, disabled=False):
    """Genera el XML para un botón."""
    text = "+ Icon" if has_icon else btn_type.capitalize()
    if btn_type == "filledTonal":
        text = "+ Icon" if has_icon else "Filled Tonal"
    name = f"btn_{btn_type}_{row}_{col}"

    enabled_prop = ""
    if disabled:
        enabled_prop = """
        <property name="enabled">
         <bool>false</bool>
        </property>"""

    icon_prop = ""
    if has_icon:
        icon_prop = """
        <property name="iconName" stdset="0">
         <string>add</string>
        </property>"""

    return f"""      <item row="{row}" column="{col}">
       <widget class="QPushButton" name="{name}">
        <property name="text">
         <string>{text}</string>
        </property>
        <property name="type" stdset="0">
         <string>{btn_type}</string>
        </property>{enabled_prop}{icon_prop}
       </widget>
      </item>
"""


# Build the grid items
items = []

# Headers (Row 0)
items.append(make_label("Text Only", 0, 1))
items.append(make_label("With Icon", 0, 2))
items.append(make_label("Disabled", 0, 3))

# Rows
types = ["elevated", "filled", "filledTonal", "outlined", "text"]
for i, t in enumerate(types):
    row = i + 1
    # Left Header
    lbl_text = "Filled Tonal" if t == "filledTonal" else t.capitalize()
    items.append(make_label(lbl_text, row, 0))
    # Text Only
    items.append(make_btn(t, row, 1, has_icon=False, disabled=False))
    # With Icon
    items.append(make_btn(t, row, 2, has_icon=True, disabled=False))
    # Disabled
    items.append(make_btn(t, row, 3, has_icon=False, disabled=True))

final_xml = xml_header + "".join(items) + xml_footer

ui_path = os.path.join(os.path.dirname(__file__), "gallery.ui")
with open(ui_path, "w", encoding="utf-8") as f:
    f.write(final_xml)

print(f"Generated {ui_path}")
