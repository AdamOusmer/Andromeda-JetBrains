# Andromeda for IntelliJ IDEA

1:1 port of the [Andromeda](https://github.com/EliverLara/Andromeda) Visual Studio Code theme to JetBrains IDEs,
built for the IntelliJ **Islands** layout (2025.2+).

## Variants

| Theme | Editor scheme | Notes |
|---|---|---|
| Andromeda | Andromeda | Base theme |
| Andromeda Italic | Andromeda Italic | Italic comments, keywords, attribute names |
| Andromeda Bordered | Andromeda Bordered | Lighter editor (`#262A33`), darker tool strips (`#20232B`), visible borders (`#1B1D23`) |
| Andromeda Italic Bordered | Andromeda Italic Bordered | Both of the above |

## Palette

| Role | Hex |
|---|---|
| Background | `#23262E` |
| Foreground | `#D5CED9` |
| Cyan (variables) | `#00E8C6` |
| Orange (numbers, properties) | `#F39C12` |
| Yellow (types, functions) | `#FFE66D` |
| Pink (`this`, headings) | `#FF00AA` |
| Hot pink (tags, interpolation) | `#F92672` |
| Purple (keywords, storage) | `#C74DED` |
| Blue (regex) | `#7CB7FF` |
| Red (constants, operators) | `#EE5D43` |
| Green (strings) | `#96E072` |
| Comment | `#A0A1A7` @ 80% |

## Build

```bash
./gradlew buildPlugin
```

Installable zip lands in `build/distributions/`. Install via *Settings → Plugins → ⚙ → Install Plugin from Disk*.

## Run in a sandbox IDE

```bash
./gradlew runIde
```

## Install into your IDE

1. `./gradlew buildPlugin` (or use the zip from `build/distributions/`).
2. *Settings → Plugins → ⚙ → Install Plugin from Disk…* → pick the zip → restart.
3. *Settings → Appearance & Behavior → Appearance → Theme* → **Andromeda Italic** (editor scheme switches automatically).

Requires the new UI with Islands layout (IntelliJ 2025.2+). The theme sets `"Islands": 1`, so the island layout switches on by itself.

## Design notes (Islands mapping)

| IntelliJ surface | Andromeda source |
|---|---|
| Window frame between islands, toolbar, status bar | `panel.border` `#1B1D23` (Bordered: `activityBar.background` `#20232B`) |
| Islands (editor, tool windows) | `editor.background` `#23262E` (Bordered editor: `#262A33`) |
| Popups / completion | `editorWidget.background` `#20232A`, border `editorSuggestWidget.border` |
| Notifications / tooltips | `notification.background` `#2D313B` |
| Inputs / combo boxes | `input.background` `#2B303B`, `dropdown.border` `#363C49` |
| List selection | `list.activeSelectionBackground` (= list bg) + cyan foreground, exactly like VS Code |
| Active editor tab | `tab.activeForeground` / `tab.activeBorder` `#00E8C6` |
| Buttons / accents | `button.background` `#00E8C5CC`, badge `#00B0FF`, progress `#C668BA` |
| Terminal | `terminal.ansi*` |

Semi-transparent VS Code colours are kept as `#RRGGBBAA` in the UI theme and composited over the editor
background in the editor scheme (IntelliJ editor schemes are opaque).

## TextMate-scope parity annotators

IntelliJ's JavaScript highlighter has no equivalent of several TextMate scopes Andromeda colours, so the plugin ships
two small annotators (active only while an Andromeda scheme is selected):

| VS Code scope | Example | Colour |
|---|---|---|
| `variable.other.object(.property)` | `execa` in `execa.stdout(...)`, `err.stderr` | Orange `#F39C12` |
| `entity.name.function` / `support.function` | `homeDir(...)`, `new Listr(...)` | Yellow `#FFE66D` |
| `constant.language` | `true` `false` `null` `undefined` (JS + Java) | Red `#EE5D43` |
| `variable.language.this` | `this` (JS) | Pink `#FF00AA` |

Brackets are silver `#BFC3CC` (also pinned for the Rainbow Brackets plugin if installed). Font: Menlo 15, line height 1.5
(VS Code's macOS defaults, sized up).

Regenerate theme files after editing the palette:

```bash
python3 tools/gen_ui.py && python3 tools/gen_scheme.py
```
