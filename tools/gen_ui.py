#!/usr/bin/env python3
"""Generate Andromeda *.theme.json island themes from JetBrains' Islands Dark base.

Strategy: keep the Islands Dark `ui` structure verbatim (so island geometry / behaviour is
identical to the built-in theme) and remap every named colour token to the Andromeda palette.
Colours are taken 1:1 from Andromeda-color-theme.json (VS Code); 8-digit hex keeps the original alpha.
"""
import json, re, sys, copy, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "src/main/resources/themes"


def load_jsonc(p):
    s = p.read_text()
    s = re.sub(r'(?m)^\s*//[^\n]*', '', s)
    s = re.sub(r'\s//[^\n"]*$', '', s, flags=re.M)
    return json.loads(s)


BASE = load_jsonc(ROOT / "base/ManyIslandsDark.theme.json")

# ---------------------------------------------------------------- Andromeda palette (VS Code)
A = dict(
    bg="#23262E", bgEditorBordered="#262A33", bgStrip="#20232B", border="#1B1D23", shadow="#14151A",
    widget="#20232A", peek="#1A1C22", input="#2B303B", inputBorder="#363C49", lineHl="#2E323D",
    whitespace="#333844", indentActive="#585C66", selection="#3D4352", drop="#3A404E",
    listFocus="#282B35", hover="#373941", ruler="#4F4355", range="#372F3C", notif="#2D313B",
    fg="#D5CED9", fgBright="#EEEEEE", muted="#999999", dim="#746F77", ignored="#555555",
    activity="#BAAFC0", white="#FFFFFF",
    cyan="#00E8C6", button="#00E8C5CC", buttonHover="#07D4B6CC", statusHover="#07D4B5B0",
    badge="#00B0FF", progress="#C668BA", link="#3B79C7",
    error="#FC644D", errorInput="#D65343", warning="#FF9F2E", warningInput="#DE9237", info="#3A6395",
    added="#9BC53D", modified="#5BC0EB", deleted="#FC644D",
    orange="#F39C12", yellow="#FFE66D", pink="#FF00AA", hotpink="#F92672", purple="#C74DED",
    blue="#7CB7FF", red="#EE5D43", green="#96E072",
    findMatch="#F39D1256", findHl="#59B8B377", findBorder="#F39D12B6",
    insertedBg="#29BF1220", removedBg="#F21B3F20",
    scrollThumb="#3A3F4C77", scrollHover="#3A3F4CAA", scrollActive="#3A3F4CCC",
)


def colors_for(variant):
    bordered = "bordered" in variant
    editor_bg = A["bgEditorBordered"] if bordered else A["bg"]
    frame = A["bgStrip"] if bordered else A["border"]
    c = {
        "white": A["white"], "black": "#000000", "transparent": editor_bg + "00",
        # --- Andromeda named palette (used by ui overrides below)
        "andromeda-bg": A["bg"], "andromeda-editor-bg": editor_bg, "andromeda-frame": frame,
        "andromeda-border": A["border"], "andromeda-cyan": A["cyan"], "andromeda-dim": A["dim"],
        # --- islands gray ramp (dark -> light) remapped onto Andromeda greys
        "gray-10": A["border"], "gray-20": A["widget"], "gray-30": A["bg"], "gray-40": A["input"],
        "gray-50": A["inputBorder"], "gray-60": A["selection"], "gray-70": A["ruler"], "gray-80": A["dim"],
        "gray-90": A["dim"], "gray-100": A["muted"], "gray-110": A["activity"], "gray-120": A["activity"],
        "gray-130": A["fg"], "gray-140": A["fg"], "gray-150": A["fgBright"], "gray-160": A["fgBright"],
        # blue ramp -> Andromeda cyan/blue accents
        "blue-10": A["listFocus"], "blue-20": A["listFocus"], "blue-30": A["selection"], "blue-40": A["selection"],
        "blue-50": A["info"], "blue-60": A["info"], "blue-70": A["link"], "blue-80": A["button"],
        "blue-90": A["badge"], "blue-100": A["blue"], "blue-110": A["blue"], "blue-120": A["blue"],
        "blue-130": A["blue"], "blue-140": A["fgBright"], "blue-150": A["fgBright"], "blue-160": A["white"],
        "green-10": A["insertedBg"], "green-20": A["insertedBg"], "green-30": A["insertedBg"], "green-40": "#29BF1240",
        "green-50": "#29BF1260", "green-60": "#9BC53D60", "green-70": "#9BC53D99", "green-80": A["added"],
        "green-90": A["added"], "green-100": A["green"], "green-110": A["green"], "green-120": A["green"],
        "green-130": A["green"], "green-140": A["green"], "green-150": A["fgBright"], "green-160": A["white"],
        "red-10": A["removedBg"], "red-20": A["removedBg"], "red-30": A["removedBg"], "red-40": "#F21B3F40",
        "red-50": "#F21B3F60", "red-60": "#D6534399", "red-70": A["errorInput"], "red-80": A["errorInput"],
        "red-90": A["error"], "red-100": A["error"], "red-110": A["error"], "red-120": A["red"],
        "red-130": A["red"], "red-140": A["red"], "red-150": A["fgBright"], "red-160": A["white"],
        "yellow-10": "#F39D1220", "yellow-20": "#F39D1230", "yellow-30": A["findMatch"], "yellow-40": "#F39D1270",
        "yellow-50": "#DE923799", "yellow-60": "#DE9237BB", "yellow-70": A["warningInput"], "yellow-80": A["warningInput"],
        "yellow-90": A["warning"], "yellow-100": A["warning"], "yellow-110": A["orange"], "yellow-120": A["yellow"],
        "yellow-130": A["yellow"], "yellow-140": A["yellow"], "yellow-150": A["fgBright"], "yellow-160": A["white"],
        "orange-10": "#F39C1220", "orange-20": "#F39C1230", "orange-30": "#F39C1240", "orange-40": "#F39C1260",
        "orange-50": "#F39C1280", "orange-60": "#F39C1299", "orange-70": "#F39C12BB", "orange-80": A["orange"],
        "orange-90": A["orange"], "orange-100": A["orange"], "orange-110": A["warning"], "orange-120": A["warning"],
        "orange-130": A["yellow"], "orange-140": A["yellow"], "orange-150": A["fgBright"], "orange-160": A["white"],
        "purple-10": A["range"], "purple-20": A["range"], "purple-30": "#C668BA40", "purple-40": "#C668BA60",
        "purple-50": "#C668BA80", "purple-60": "#C668BA99", "purple-70": A["progress"], "purple-80": A["progress"],
        "purple-90": A["purple"], "purple-100": A["purple"], "purple-110": A["purple"], "purple-120": A["purple"],
        "purple-130": A["purple"], "purple-140": A["fgBright"], "purple-150": A["fgBright"], "purple-160": A["white"],
        "teal-10": "#00E8C620", "teal-20": "#00E8C630", "teal-30": A["findHl"], "teal-40": "#00E8C660",
        "teal-50": "#00E8C680", "teal-60": "#00E8C699", "teal-70": A["statusHover"], "teal-80": A["button"],
        "teal-90": A["cyan"], "teal-100": A["cyan"], "teal-110": A["cyan"], "teal-120": A["cyan"],
        "teal-130": A["cyan"], "teal-140": A["fgBright"], "teal-150": A["fgBright"], "teal-160": A["white"],
        "transparent-white-10": "#FFFFFF10", "transparent-white-20": "#FFFFFF17", "transparent-white-30": "#FFFFFF21",
        "transparent-white-40": "#FFFFFF29", "transparent-white-50": "#FFFFFF3B",
        "transparent-black-10": "#00000008", "transparent-black-20": "#00000012", "transparent-black-30": "#00000020",
        "transparent-black-40": "#00000030", "transparent-black-50": "#00000045",
        # --- semantic tokens
        "text-default": A["fg"], "text-muted": A["muted"], "text-secondary": A["dim"], "text-disabled": A["ignored"],
        "text-over-accent": A["white"], "text-over-accent-inverted": A["bgStrip"], "text-link": A["link"],
        "text-error": A["error"], "text-warning": A["warning"], "text-success": A["green"], "editor-text": A["fg"],
        "layer-0-bg": editor_bg, "layer-0-border": A["border"], "layer-0-bg-inline": A["input"], "layer-0-border-inline": A["inputBorder"],
        "layer-1-bg": A["widget"], "layer-1-border": A["range"], "layer-1-bg-inline": A["input"], "layer-1-border-inline": A["inputBorder"],
        "layer-2-bg": A["notif"], "layer-2-bg-inline": A["input"], "layer-2-border": A["inputBorder"], "layer-2-border-inline": A["ruler"],
        "accent-brand-bg": A["button"], "accent-brand-border": A["button"],
        "accent-brand-bg-secondary": A["info"], "accent-brand-border-secondary": A["info"],
        "accent-error-bg": A["error"], "accent-error-border": A["error"],
        "accent-error-bg-secondary": A["errorInput"], "accent-error-border-secondary": A["errorInput"],
        "accent-warning-bg": A["warning"], "accent-warning-border": A["warning"],
        "accent-warning-bg-secondary": A["warningInput"], "accent-warning-border-secondary": A["warningInput"],
        "accent-success-bg": A["added"], "accent-success-border": A["added"],
        "accent-success-bg-secondary": "#9BC53DBB", "accent-success-border-secondary": "#9BC53DBB",
        "accent-neutral-bg": A["dim"], "accent-ai-bg": A["range"], "accent-ai-border": A["progress"],
        "core-bg-transparent-hovered": "#5A5D5E50", "core-bg-transparent-pressed": "#63666750", "core-border-transparent": "#FFFFFF21",
        "dialog-bg": A["bg"], "dialog-bg-inline": A["input"], "dialog-border": A["border"],
        "popup-bg": A["widget"], "popup-bg-inline": A["widget"], "popup-border": A["range"], "popup-border-inline": A["range"],
        "editor-bg": editor_bg, "editor-bg-inline": A["input"], "editor-border": A["border"], "editor-border-inline": A["inputBorder"],
        "editor-border-alt": A["border"],
        "tool-window-bg": A["bg"], "tool-window-bg-inline": A["input"], "tool-window-bg-alt": A["bg"],
        "tool-window-border": A["border"], "tool-window-border-inline": A["inputBorder"],
        "main-window-bg": frame, "main-window-bg-alt": frame, "main-window-border": A["border"],
        "control-bg": A["input"], "control-bg-disabled": A["bg"], "control-bg-raised": A["input"],
        "control-border": A["inputBorder"], "control-border-disabled": A["lineHl"], "control-border-raised": A["dim"],
        "control-border-over-accent": "#FFFFFF3B", "control-bg-small": A["whitespace"], "control-bg-small-disabled": A["lineHl"],
        "control-border-small": A["dim"],
        "control-brand-bg": A["button"], "control-brand-border": A["button"],
        "control-error-bg": A["errorInput"], "control-error-border": A["errorInput"], "control-error-border-secondary": "#D6534399",
        "control-warning-bg": A["warningInput"], "control-warning-border": A["warningInput"], "control-warning-border-secondary": "#DE923799",
        "control-success-bg": A["added"], "control-success-border": A["added"],
        "toolbar-bg-hovered": "#5A5D5E50", "toolbar-bg-pressed": "#63666750", "toolbar-border": "#FFFFFF21",
        "toolbar-selected-bg": A["selection"], "toolbar-selected-bg-hovered": A["ruler"], "toolbar-selected-bg-active": A["listFocus"],
        "toolbar-run-bg": A["added"], "toolbar-run-bg-hovered": "#9BC53DBB", "toolbar-stop-bg": A["error"], "toolbar-stop-bg-hovered": A["errorInput"],
        "feedback-bg": A["notif"], "feedback-border": A["notif"], "feedback-bg-inline": A["input"],
        "feedback-brand-bg": A["info"], "feedback-brand-border": A["info"],
        "feedback-success-bg": "#9BC53DBB", "feedback-success-border": "#9BC53DBB",
        "feedback-warning-bg": A["warningInput"], "feedback-warning-border": A["warningInput"],
        "feedback-error-bg": A["errorInput"], "feedback-error-border": A["errorInput"],
        "feedback-control-border": "#FFFFFF3B", "feedback-ai-bg": A["range"], "feedback-ai-border": A["progress"],
        # Andromeda lists: selection bg == list bg, cyan text (list.activeSelectionBackground = #23262E)
        "selection-bg-active": A["bg"], "selection-bg-active-muted": A["listFocus"], "selection-bg-inactive": A["bg"],
        "selection-bg-hovered": A["bg"],
        "tab-selected-bg-active": A["bgEditorBordered"] if bordered else A["bg"], "tab-selected-bg-inactive": A["bg"],
        "tab-selected-border-active": A["cyan"], "tab-selected-border-inactive": "#00E8C680",
        "tab-bg-hovered": editor_bg + "00", "tab-file-color-mask-bg": editor_bg + "80",
        "got-it-bg": A["info"], "got-it-border": A["info"], "got-it-text-link": A["blue"], "got-it-text-step": A["activity"],
        "got-it-shortcut-bg": "#3B79C7BB", "got-it-code-border": "#FFFFFF70", "got-it-contrast-button-bg": "#3B79C7BB",
        "inlay-bg": "#FFFFFF21", "inlay-border": "#FFFFFF3B",
        "toggle-off-bg": A["input"], "toggle-button-bg": A["dim"], "toggle-border": A["dim"],
        "editor-floating-toolbar-bg": A["widget"], "popup-completion-match-text": "#2AAAFF",
        "presentation-assistant-bg": A["info"], "search-match-bg": A["findHl"], "tree-indent-guide-border": A["whitespace"],
        "icon-default-stroke": A["activity"], "icon-over-accent": A["white"], "icon-green-stroke": A["green"],
    }
    # legacy ExperimentalDark (parent theme) ramps — inherited ui keys resolve through these
    legacy = {
        "Gray1": A["border"], "Gray2": A["bg"], "Gray3": A["input"], "Gray4": A["inputBorder"], "Gray5": A["selection"],
        "Gray6": A["ruler"], "Gray7": A["indentActive"], "Gray8": A["dim"], "Gray9": A["muted"], "Gray10": A["activity"],
        "Gray11": A["fg"], "Gray12": A["fg"], "Gray13": A["fgBright"], "Gray14": A["white"],
        "Blue1": A["listFocus"], "Blue2": A["selection"], "Blue3": A["info"], "Blue4": A["info"], "Blue5": A["link"],
        "Blue6": A["button"], "Blue7": A["buttonHover"], "Blue8": A["badge"], "Blue9": A["blue"], "Blue10": A["blue"],
        "Blue11": A["blue"], "Blue12": A["blue"], "Blue13": A["fgBright"],
        "Green1": A["insertedBg"], "Green2": A["insertedBg"], "Green3": "#29BF1240", "Green4": "#29BF1260", "Green5": "#9BC53D99",
        "Green6": A["added"], "Green7": A["green"], "Green8": A["green"], "Green9": A["green"], "Green10": A["green"],
        "Green11": A["green"], "Green12": A["fgBright"],
        "Yellow1": "#F39D1230", "Yellow2": A["findMatch"], "Yellow3": "#F39D1270", "Yellow4": "#DE923799", "Yellow5": A["orange"],
        "Yellow6": A["warning"], "Yellow7": A["yellow"], "Yellow8": A["yellow"], "Yellow9": A["yellow"], "Yellow10": A["yellow"],
        "Yellow11": A["fgBright"],
        "Red1": A["removedBg"], "Red2": A["removedBg"], "Red3": "#F21B3F40", "Red4": "#F21B3F60", "Red5": "#D6534399",
        "Red6": A["errorInput"], "Red7": A["error"], "Red8": A["error"], "Red9": A["red"], "Red10": A["red"],
        "Red11": A["red"], "Red12": A["fgBright"],
        "Orange1": "#F39C1230", "Orange2": "#F39C1240", "Orange3": "#F39C1260", "Orange4": "#F39C1280", "Orange5": "#F39C1299",
        "Orange6": A["orange"], "Orange7": A["orange"], "Orange8": A["warning"], "Orange9": A["warning"], "Orange10": A["yellow"],
        "Orange11": A["fgBright"],
        "Purple1": A["range"], "Purple2": A["range"], "Purple3": "#C668BA40", "Purple4": "#C668BA60", "Purple5": "#C668BA80",
        "Purple6": "#C668BA99", "Purple7": A["progress"], "Purple8": A["progress"], "Purple9": A["purple"], "Purple10": A["purple"],
        "Purple11": A["purple"], "Purple12": A["fgBright"],
        "Teal1": "#00E8C620", "Teal2": A["findHl"], "Teal3": "#00E8C640", "Teal4": "#00E8C660", "Teal5": "#00E8C680",
        "Teal6": "#00E8C699", "Teal7": A["cyan"], "Teal8": A["cyan"], "Teal9": A["cyan"], "Teal10": A["cyan"],
        "Teal11": A["cyan"], "Teal12": A["fgBright"],
    }
    c.update(legacy)
    # gradients (registry-gated, off by default) — keep JetBrains values
    for k, v in BASE["colors"].items():
        if k.startswith("grad-"):
            c[k] = v
    missing = [k for k in BASE["colors"] if k not in c]
    assert not missing, f"unmapped islands colour tokens: {missing}"
    return c


def ui_overrides(variant):
    bordered = "bordered" in variant
    return {
        "*": {
            "selectionForeground": "andromeda-cyan",
            "selectionInactiveForeground": "andromeda-cyan",
            "focusColor": "andromeda-dim",
            "underlineColor": "andromeda-cyan",
        },
        "Counter": {"background": "#00B0FF", "foreground": "#20232B"},
        "Badge": {
            "blueSecondaryBackground": "#3A6395B3", "blueSecondaryForeground": "#7CB7FF",
            "blueBackground": "#00B0FF", "blueForeground": "#20232B",
            "greenSecondaryBackground": "#9BC53DB3", "greenSecondaryForeground": "#96E072",
            "greenBackground": "#96E072", "greenForeground": "#20232B",
            "purpleSecondaryBackground": "#C668BAB3", "purpleSecondaryForeground": "#C74DED",
        },
        "ProgressBar": {
            "progressColor": "#C668BA", "indeterminateStartColor": "#C668BA", "indeterminateendcolor": "#C668BA",
            "indeterminateEndColor": "#C668BA", "progressCounterBackground": "#C668BA", "trackColor": "#333844",
        },
        "Button": {
            "default": {
                "startBackground": "#00E8C5CC", "endBackground": "#00E8C5CC",
                "startBorderColor": "#00E8C5CC", "endBorderColor": "#00E8C5CC",
            }
        },
        "Link": {
            "activeForeground": "#3B79C7", "hoverForeground": "#3B79C7", "pressedForeground": "#3B79C7",
            "visitedForeground": "#3B79C7", "secondaryForeground": "#3B79C7",
        },
        "ScrollBar": {
            "thumbColor": "#3A3F4C77", "thumbBorderColor": "#3A3F4C77",
            "hoverThumbColor": "#3A3F4CAA", "hoverThumbBorderColor": "#3A3F4CAA",
            "trackColor": "#3A3F4C00", "hoverTrackColor": "#3A3F4C00",
            "Transparent": {
                "thumbColor": "#3A3F4C77", "thumbBorderColor": "#3A3F4C00",
                "hoverThumbColor": "#3A3F4CAA", "hoverThumbBorderColor": "#3A3F4CAA",
                "trackColor": "#3A3F4C00", "hoverTrackColor": "#3A3F4C1A",
            },
        },
        "EditorTabs": {
            "underlinedTabForeground": "#00E8C6", "underlinedTabBackground": "andromeda-editor-bg",
            "underlinedBorderColor": "#00E8C6", "inactiveUnderlinedTabBorderColor": "#00E8C680",
            "inactiveUnderlinedTabBackground": "andromeda-editor-bg",
            "underlineColor": "#00E8C6", "inactiveUnderlineColor": "#00E8C680",
            "hoverBackground": "#00E8C600", "hoverInactiveBackground": "#00E8C600",
            "unselectedAlpha": 1.0, "unselectedBlend": 1.0,
        },
        "Label": {"foreground": "#D5CED9"},
        "ToolWindow": {
            "Button": {
                "foreground": "#BAAFC099", "selectedForeground": "#BAAFC0", "selectedBackground": "#282B35",
                "DragAndDrop": {"buttonDropBackground": "#3A404E", "stripeBackground": "andromeda-frame"},
            },
            "DragAndDrop": {"areaBackground": "#495061D7"},
            "HeaderTab": {"underlineColor": "#00E8C6", "inactiveUnderlineColor": "#00E8C680",
                          "selectedForeground": "#00E8C6", "selectedInactiveForeground": "#00E8C6"},
            "Header": {"background": "andromeda-bg", "inactiveBackground": "andromeda-bg", "foreground": "#00E8C6"},
        },
        "StatusBar": {
            "Widget": {"foreground": "#999999", "hoverForeground": "#EEEEEE",
                       "hoverBackground": "#07D4B5B0", "pressedBackground": "#00E8C5CC"},
            "Breadcrumbs": {"foreground": "#746F77", "hoverForeground": "#D5CED9",
                            "hoverBackground": "#07D4B5B0", "pressedBackground": "#00E8C5CC",
                            "selectionBackground": "#07D4B5B0", "selectionInactiveBackground": "#07D4B5B0"},
        },
        "Debugger": {
            "Variables": {"valueForeground": "#F39C12", "collectingDataForeground": "#746F77",
                          "evaluatingExpressionForeground": "#746F77", "changedValueForeground": "#7CB7FF",
                          "modifyingValueForeground": "#7CB7FF", "typeForeground": "#746F77"},
        },
        "Slider": {"buttonColor": "#D5CED9", "buttonBorderColor": "#23262E", "tickColor": "#746F77", "trackColor": "#3D4352"},
        "List": {"Tag": {"background": "#3D4352", "foreground": "#999999"}},
        "Review": {"Branch": {"Background": "#3D4352", "Background.Hover": "#4F4355"},
                   "State": {"Background": "#4F4355", "Foreground": "#999999"},
                   "ChatItem": {"Hover": "#5A5D6333"}},
        "Editor": {"ToolTip": {"selectionBackground": "#373941"}},
        "DragAndDrop": {"rowBackground": "#3A404E", "areaBackground": "#495061D7"},
        "ComboPopup.border": "1,1,1,1,#363C49",
        "Window.undecorated.border": "1,1,1,1,#363C49",
        "MainWindow.Tab": {"background": "#14151A"},
        "MainWindow.FullScreeControl.Background": "#746F77",
        "VersionControl": {
            "Log": {"Commit": {"currentBranchBackground": "#2E323D", "unmatchedForeground": "#746F77",
                               "Reference.foreground": "#746F77"}},
            "FileHistory.Commit.selectedBranchBackground": "#2E323D",
            "MarkerPopup": {"borderColor": "#363C49"},
            "GitLog": {"headIconColor": "#FFE66D", "localBranchIconColor": "#96E072", "otherIconColor": "#746F77",
                       "remoteBranchIconColor": "#C74DED", "tagIconColor": "#746F77"},
            "Merge.Status.NoConflicts.foreground": "#96E072",
        },
        "FileColor": {"Yellow": "#3D3223", "Green": "#24392A", "Orange": "#45322B", "Rose": "#3D2530",
                      "Violet": "#372F3C", "Blue": "#1D3D3B", "Gray": "#2E323D"},
        "LineProfiler": {"Line": {"labelBackground": "#FFFFFF17", "foreground": "#999999", "hoverBackground": "#FFFFFF29"},
                         "HotLine": {"labelBackground": "#3D2530", "foreground": "#FC644D", "hoverBackground": "#59263F"},
                         "IgnoredLine": {"labelBackground": "#FFFFFF29", "foreground": "#746F77"}},
        "TrialWidget": {
            "Default": {"foreground": "#D5CED9", "background": "#2B303B", "borderColor": "#746F77",
                        "hoverForeground": "#D5CED9", "hoverBackground": "#3D4352", "hoverBorderColor": "#746F77"},
            "Active": {"foreground": "#96E072", "background": "#24392A", "borderColor": "#9BC53D",
                       "hoverForeground": "#96E072", "hoverBackground": "#29BF1240", "hoverBorderColor": "#9BC53D"},
            "Alert": {"foreground": "#FFE66D", "background": "#3D3223", "borderColor": "#DE9237",
                      "hoverForeground": "#FFE66D", "hoverBackground": "#694E25", "hoverBorderColor": "#DE9237"},
            "Expiring": {"foreground": "#FC644D", "background": "#3D2530", "borderColor": "#D65343",
                         "hoverForeground": "#FC644D", "hoverBackground": "#59263F", "hoverBorderColor": "#D65343"},
            "Progress": {"foreground": "#999999", "background": "#2B303B", "borderColor": "#746F77",
                         "hoverForeground": "#999999", "hoverBackground": "#2B303B", "hoverBorderColor": "#746F77"},
        },
        "UnattendedHostStatus": {"warningBackground": "#FF9F2E", "warningForeground": "#20232B", "dangerBackground": "#FC644D"},
        "PresentationAssistant": {"Pale": {"Popup": {"border": "#3D4352"}, "PopupBackground": "#3D4352", "keymapLabel": "#999999"}},
        "HelpBrowser": {"titleHighlightForeground": "#3B79C7"},
        "DataSummary.Chart.barColor": "#00B0FF",
        "ManagedIdeBadgeBorder": "#363C49", "ManagedIdeBadgeBackground": "#2B303B",
        "ManagedIdeBadgeBackgroundHover": "#3D4352", "ManagedIdeMenuItemHover": "#3D4352",
        "NuGet": {"section": {"background": "#23262E", "hoverBackground": "#282B35"}},
        "Lesson": {"shortcutBackground": "#3D4352"},
        "WelcomeScreen": {"Projects": {"actions": {"background": "#2B303B"}}},
        "RunWidget": {"hoverBackground": "#00000019", "pressedBackground": "#00000028"},
        # Islands geometry stays JetBrains-default; only colour changes.
        "Island": {"borderColor": "tool-window-bg"},
        # Bordered variant: Andromeda draws 1px #1B1D23 borders around side bar / activity bar.
        **({"Borders.color": "#1B1D23", "Borders.ContrastBorderColor": "#1B1D23",
            "ToolWindow.Header.borderColor": "#1B1D23", "EditorTabs.underTabsBorderColor": "#1B1D23"} if bordered else {}),
    }


def deep_merge(dst, src):
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            deep_merge(dst[k], v)
        else:
            dst[k] = v
    return dst


VARIANTS = {
    "Andromeda": ("Andromeda", "Andromeda"),
    "AndromedaItalic": ("Andromeda Italic", "Andromeda Italic"),
    "AndromedaBordered": ("Andromeda Bordered", "Andromeda Bordered"),
    "AndromedaItalicBordered": ("Andromeda Italic Bordered", "Andromeda Italic Bordered"),
}


def build(file_stem, name, scheme):
    variant = file_stem.lower()
    t = {
        "name": name,
        "dark": True,
        "author": "EliverLara (port by AdamOusmer)",
        "parentTheme": "ExperimentalDark",
        "editorScheme": scheme,
        "colors": colors_for(variant),
        "ui": deep_merge(copy.deepcopy(BASE["ui"]), ui_overrides(variant)),
        "icons": copy.deepcopy(BASE["icons"]),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{file_stem}.theme.json").write_text(json.dumps(t, indent=2) + "\n")
    print("wrote", OUT / f"{file_stem}.theme.json")


if __name__ == "__main__":
    for stem, (name, scheme) in VARIANTS.items():
        build(stem, name, scheme)
