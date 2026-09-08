#!/usr/bin/env python3
"""Generate Andromeda editor colour schemes (.xml, ICLS) — 1:1 mapping of Andromeda's VS Code
tokenColors / editor colours onto IntelliJ attribute keys. Alpha colours are composited over the
editor background because editor-scheme values are opaque RRGGBB."""
import pathlib, sys
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "src/main/resources/themes"

# ---- Andromeda palette --------------------------------------------------------------------
BG = "23262E"; BG_BORDERED = "262A33"
FG = "D5CED9"
CYAN = "00E8C6"; ORANGE = "F39C12"; YELLOW = "FFE66D"; PINK = "FF00AA"; HOTPINK = "F92672"
PURPLE = "C74DED"; BLUE = "7CB7FF"; RED = "EE5D43"; GREEN = "96E072"
DIM = "746F77"; ERROR = "FC644D"; WARNING = "FF9F2E"; INFO = "3B79C7"; MUTED = "999999"


def blend(fg_rgba, bg):
    """Composite #RRGGBBAA (or RRGGBB) over RRGGBB -> RRGGBB."""
    s = fg_rgba.lstrip("#")
    r, g, b = int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    a = int(s[6:8], 16) / 255 if len(s) == 8 else 1.0
    br, bgc, bb = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
    return "%02X%02X%02X" % (round(r * a + br * (1 - a)), round(g * a + bgc * (1 - a)), round(b * a + bb * (1 - a)))


def build(name, bordered, italic):
    bg = BG_BORDERED if bordered else BG
    B = lambda c: blend(c, bg)
    COMMENT = B("A0A1A7CC")
    I = 2 if italic else 0  # FONT_TYPE 2 = italic

    colors = {
        # editor chrome (VS Code key in comment)
        "CARET_COLOR": "FFFFFF",                       # editorCursor.foreground
        "CARET_ROW_COLOR": "2E323D",                   # editor.lineHighlightBackground
        "SELECTION_BACKGROUND": "3D4352",              # editor.selectionBackground
        "SELECTION_FOREGROUND": "",
        "LINE_NUMBERS_COLOR": DIM,                     # editorLineNumber.foreground
        "LINE_NUMBER_ON_CARET_ROW_COLOR": FG,          # editorLineNumber.activeForeground (VS default = fg)
        "GUTTER_BACKGROUND": bg,
        "EDITOR_GUTTER_BACKGROUND": bg,
        "CONSOLE_BACKGROUND_KEY": bg,                  # terminal.background = editor.background
        "WHITESPACES": "333844",                       # editorWhitespace.foreground
        "INDENT_GUIDE": "333844",                      # editorIndentGuide.background
        "SELECTED_INDENT_GUIDE": "585C66",             # editorIndentGuide.activeBackground
        "VISUAL_INDENT_GUIDE": "333844",
        "MATCHED_BRACES_INDENT_GUIDE_COLOR": "585C66",
        "RIGHT_MARGIN_COLOR": "4F4355",                # editorRuler.foreground
        "TEARLINE_COLOR": "1B1D23",                    # panel.border
        "SOFT_WRAP_SIGN_COLOR": DIM,
        "METHOD_SEPARATORS_COLOR": "333844",
        "FOLDED_TEXT_BORDER_COLOR": DIM,
        "ADDED_LINES_COLOR": B("9BC53DBB"),            # editorGutter.addedBackground
        "MODIFIED_LINES_COLOR": B("5BC0EBBB"),         # editorGutter.modifiedBackground
        "DELETED_LINES_COLOR": B("FC644DBB"),          # editorGutter.deletedBackground
        "WHITESPACES_MODIFIED_LINES_COLOR": B("5BC0EB60"),
        "IGNORED_ADDED_LINES_BORDER_COLOR": B("9BC53DBB"),
        "IGNORED_MODIFIED_LINES_BORDER_COLOR": B("5BC0EBBB"),
        "IGNORED_DELETED_LINES_BORDER_COLOR": B("FC644DBB"),
        "DIFF_SEPARATORS_BACKGROUND": "1B1D23",
        "ANNOTATIONS_COLOR": DIM,
        "ANNOTATIONS_LAST_COMMIT_COLOR": FG,
        "VCS_ANNOTATIONS_COLOR_1": "2E323D", "VCS_ANNOTATIONS_COLOR_2": "2B2E38", "VCS_ANNOTATIONS_COLOR_3": "282B34",
        "VCS_ANNOTATIONS_COLOR_4": "262930", "VCS_ANNOTATIONS_COLOR_5": bg,
        "DOCUMENTATION_COLOR": "373941",               # editorHoverWidget.background
        "LOOKUP_COLOR": "20232A",                      # editorSuggestWidget.background
        "INFORMATION_HINT": "373941",                  # editorHoverWidget.background
        "QUESTION_HINT": "3A6395",                     # inputValidation.infoBackground
        "ERROR_HINT": "D65343",                        # inputValidation.errorBackground
        "NOTIFICATION_BACKGROUND": "2D313B",           # notification.background
        "PROMOTION_PANE": "3A6395",
        "HINT_BORDER": B("00E8C5CC"),                  # editorHoverWidget.border
        "RECENT_LOCATIONS_SELECTION": "282B35",
        "INLINE_REFACTORING_SETTINGS_DEFAULT": "2B303B", "INLINE_REFACTORING_SETTINGS_FOCUSED": "2B303B",
        "INLINE_REFACTORING_SETTINGS_HOVERED": "373941",
        "DOC_COMMENT_GUIDE": "333844", "DOC_COMMENT_LINK": INFO,
        "ScrollBar.Mac.thumbColor": "3A3F4C77", "ScrollBar.Mac.hoverThumbColor": "3A3F4CAA",
        "ScrollBar.thumbColor": "3A3F4C77", "ScrollBar.hoverThumbColor": "3A3F4CAA",
        "ScrollBar.Mac.Transparent.thumbColor": "3A3F4C77", "ScrollBar.Mac.Transparent.hoverThumbColor": "3A3F4CAA",
        "ScrollBar.Transparent.thumbColor": "3A3F4C77", "ScrollBar.Transparent.hoverThumbColor": "3A3F4CAA",
        "STICKY_LINES_BORDER_COLOR": "1B1D23",
        "STICKY_LINES_BACKGROUND": bg,
        "STICKY_LINES_HOVERED_COLOR": "2E323D",
        "BREADCRUMBS_BACKGROUND": bg,
        # file status colours (project tree) — gitDecoration.* (Andromeda sets ignored only; rest VS defaults)
        "FILESTATUS_ADDED": "81B88B", "FILESTATUS_COPIED": "81B88B", "FILESTATUS_addedOutside": "81B88B",
        "FILESTATUS_MODIFIED": "E2C08D", "FILESTATUS_modifiedOutside": "E2C08D", "FILESTATUS_RENAMED": "E2C08D",
        "FILESTATUS_NOT_CHANGED_IMMEDIATE": "E2C08D", "FILESTATUS_NOT_CHANGED_RECURSIVE": "E2C08D",
        "FILESTATUS_DELETED": "C74E39", "FILESTATUS_IDEA_FILESTATUS_DELETED_FROM_FILE_SYSTEM": "C74E39",
        "FILESTATUS_UNKNOWN": "73C991",
        "FILESTATUS_IDEA_FILESTATUS_IGNORED": "555555",
        "FILESTATUS_MERGED": "C74DED",
        "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_CONFLICTS": "E4676B",
        "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_BOTH_CONFLICTS": "E4676B",
        "FILESTATUS_IDEA_FILESTATUS_MERGED_WITH_PROPERTY_CONFLICTS": "E4676B",
        "FILESTATUS_changelistConflict": "E4676B",
    }

    def attr(fg=None, bg_=None, ft=None, effect=None, effect_type=None, error_stripe=None, base=None):
        d = {}
        if fg is not None: d["FOREGROUND"] = fg
        if bg_ is not None: d["BACKGROUND"] = bg_
        if ft is not None: d["FONT_TYPE"] = str(ft)
        if effect is not None: d["EFFECT_COLOR"] = effect
        if effect_type is not None: d["EFFECT_TYPE"] = str(effect_type)
        if error_stripe is not None: d["ERROR_STRIPE_COLOR"] = error_stripe
        if base is not None: d["__base__"] = base
        return d

    UNDERLINE, BOLD_LINE, UNDERWAVE, BORDER, STRIKE, DOTTED = 1, 2, 4, 5, 3, 6  # EFFECT_TYPE values

    attrs = {
        # ---- text & defaults (tokenColors[0]) --------------------------------------------
        "TEXT": attr(FG, bg),
        "DEFAULT_LINE_COMMENT": attr(COMMENT, ft=I),
        "DEFAULT_BLOCK_COMMENT": attr(COMMENT, ft=I),
        "DEFAULT_DOC_COMMENT": attr(COMMENT, ft=I),
        "DEFAULT_DOC_MARKUP": attr(COMMENT, ft=I),
        "DEFAULT_DOC_COMMENT_TAG": attr(COMMENT, ft=I | 1),
        "DEFAULT_DOC_COMMENT_TAG_VALUE": attr(CYAN, ft=I),
        "DEFAULT_COMMA": attr(FG), "DEFAULT_SEMICOLON": attr(FG), "DEFAULT_DOT": attr(FG),
        "DEFAULT_BRACES": attr(FG), "DEFAULT_BRACKETS": attr(FG), "DEFAULT_PARENTHS": attr(FG),
        "DEFAULT_OPERATION_SIGN": attr(RED),           # keyword.operator -> Red
        "DEFAULT_KEYWORD": attr(PURPLE, ft=I),         # keyword / storage -> Purple
        "DEFAULT_STRING": attr(GREEN),                 # string -> Green
        "DEFAULT_VALID_STRING_ESCAPE": attr(GREEN),
        "DEFAULT_INVALID_STRING_ESCAPE": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        "DEFAULT_NUMBER": attr(ORANGE),                # constant.numeric -> Orange
        "DEFAULT_CONSTANT": attr(RED),                 # constant -> Red
        "DEFAULT_PREDEFINED_SYMBOL": attr(YELLOW),     # support.function -> Yellow
        "DEFAULT_IDENTIFIER": attr(CYAN),              # variable -> Cyan
        "DEFAULT_LOCAL_VARIABLE": attr(CYAN),
        "DEFAULT_REASSIGNED_LOCAL_VARIABLE": attr(CYAN, effect=DIM, effect_type=UNDERLINE),
        "DEFAULT_GLOBAL_VARIABLE": attr(CYAN),
        "DEFAULT_PARAMETER": attr(CYAN),
        "DEFAULT_REASSIGNED_PARAMETER": attr(CYAN, effect=DIM, effect_type=UNDERLINE),
        "DEFAULT_INSTANCE_FIELD": attr(ORANGE),        # variable.other.object.property -> Orange
        "DEFAULT_STATIC_FIELD": attr(ORANGE),
        "DEFAULT_FUNCTION_DECLARATION": attr(YELLOW),  # entity.name.function -> Yellow
        "DEFAULT_FUNCTION_CALL": attr(YELLOW),
        "DEFAULT_INSTANCE_METHOD": attr(YELLOW),
        "DEFAULT_STATIC_METHOD": attr(YELLOW),
        "DEFAULT_CLASS_NAME": attr(YELLOW),            # entity.name.type -> Yellow
        "DEFAULT_CLASS_REFERENCE": attr(YELLOW),
        "DEFAULT_INTERFACE_NAME": attr(YELLOW),
        "DEFAULT_METADATA": attr(PURPLE),              # storage.type.annotation -> Purple
        "DEFAULT_LABEL": attr(FG),
        "DEFAULT_TAG": attr(HOTPINK),                  # entity.name.tag -> Hot Pink
        "DEFAULT_ATTRIBUTE": attr(YELLOW, ft=I),       # entity.other.attribute-name -> Yellow (italic variant)
        "DEFAULT_ENTITY": attr(CYAN),                  # constant.character.entity.html -> Cyan
        "DEFAULT_TEMPLATE_LANGUAGE_COLOR": attr(bg_="2E323D"),
        "DEFAULT_HIGHLIGHTED_REFERENCE": attr(effect=DIM, effect_type=UNDERLINE),
        "DEFAULT_INLINE_PARAMETER_HINT": attr(DIM, "2B303B"),
        "INLINE_PARAMETER_HINT": attr(DIM, "2B303B"),
        "INLINE_PARAMETER_HINT_CURRENT": attr(FG, "3D4352"),
        "INLINE_PARAMETER_HINT_HIGHLIGHTED": attr(FG, "3D4352"),
        "INLAY_DEFAULT": attr(DIM, "2B303B"),
        "INLAY_TEXT_WITHOUT_BACKGROUND": attr(DIM),
        "INLAY_BUTTON_DEFAULT": attr(FG, "2B303B", effect="363C49"),
        "INLAY_BUTTON_FOCUSED": attr(FG, "3D4352", effect=DIM),
        "INLAY_BUTTON_HOVERED": attr(FG, "373941", effect=DIM),
        "INLINE_REFACTORING_SETTINGS_DEFAULT": attr(FG, "2B303B"),
        "CODE_LENS_BORDER_COLOR": attr(DIM),
        "FOLDED_TEXT_ATTRIBUTES": attr(DIM, "2E323D"),
        # ---- editor highlights ------------------------------------------------------------
        "IDENTIFIER_UNDER_CARET_ATTRIBUTES": attr(bg_="4F4355", error_stripe="4F4355"),          # editor.wordHighlightBackground
        "WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES": attr(bg_=B("DB45A280"), error_stripe=B("DB45A280")),  # wordHighlightStrong
        "SEARCH_RESULT_ATTRIBUTES": attr(bg_=B("59B8B377"), error_stripe=B("59B8B377")),          # editor.findMatchHighlightBackground
        "TEXT_SEARCH_RESULT_ATTRIBUTES": attr(bg_=B("F39D1256"), effect=B("F39D12B6"), effect_type=BORDER, error_stripe=B("F39D12B6")),  # findMatch + border
        "MATCHED_BRACE_ATTRIBUTES": attr(bg_=DIM, effect=DIM, effect_type=BORDER, ft=1),           # editorBracketMatch
        "UNMATCHED_BRACE_ATTRIBUTES": attr(bg_=B("FC644D40"), effect=ERROR, effect_type=BORDER),
        "ERRORS_ATTRIBUTES": attr(effect=ERROR, effect_type=UNDERWAVE, error_stripe=ERROR),        # editorError.foreground
        "WARNING_ATTRIBUTES": attr(effect=WARNING, effect_type=UNDERWAVE, error_stripe=WARNING),   # editorWarning.foreground
        "WEAK_WARNING_ATTRIBUTES": attr(effect=B("FF9F2EAA"), effect_type=UNDERWAVE, error_stripe=B("FF9F2EAA")),
        "INFO_ATTRIBUTES": attr(effect=INFO, effect_type=UNDERWAVE, error_stripe=INFO),            # editorInfo (VS default blue)
        "GENERIC_SERVER_ERROR_OR_WARNING": attr(effect=WARNING, effect_type=UNDERWAVE, error_stripe=WARNING),
        "DUPLICATE_FROM_SERVER": attr(bg_="2E323D"),
        "TYPO": attr(effect=B("96E072AA"), effect_type=UNDERWAVE),
        "NOT_USED_ELEMENT_ATTRIBUTES": attr(DIM),
        "WRONG_REFERENCES_ATTRIBUTES": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        "MARKED_FOR_REMOVAL_ATTRIBUTES": attr(effect=ERROR, effect_type=STRIKE),
        "DEPRECATED_ATTRIBUTES": attr(effect=FG, effect_type=STRIKE),
        "RUNTIME_ERROR": attr(effect=ERROR, effect_type=UNDERWAVE, error_stripe=ERROR),
        "TODO_DEFAULT_ATTRIBUTES": attr(YELLOW, ft=I | 1, error_stripe=YELLOW),
        "BOOKMARKS_ATTRIBUTES": attr(error_stripe=CYAN),
        "BREAKPOINT_ATTRIBUTES": attr(bg_=B("FC644D40"), error_stripe=ERROR),
        "EXECUTIONPOINT_ATTRIBUTES": attr(FG, B("FFE66D40"), error_stripe=YELLOW),
        "DEBUGGER_INLINED_VALUES": attr(DIM, ft=I),
        "DEBUGGER_INLINED_VALUES_MODIFIED": attr(BLUE, ft=I),
        "DEBUGGER_INLINED_VALUES_EXECUTION_LINE": attr(ORANGE, ft=I),
        "DEBUGGER_SMART_STEP_INTO_TARGET": attr(bg_="3D4352", effect=DIM, effect_type=BORDER),
        "DEBUGGER_SMART_STEP_INTO_SELECTION": attr(bg_="3D4352", effect=CYAN, effect_type=BORDER),
        "LINE_FULL_COVERAGE": attr(B("9BC53DBB"), error_stripe=B("9BC53DBB")),
        "LINE_PARTIAL_COVERAGE": attr(WARNING, error_stripe=WARNING),
        "LINE_NONE_COVERAGE": attr(ERROR, error_stripe=ERROR),
        "LIVE_TEMPLATE_ATTRIBUTES": attr(effect=CYAN, effect_type=BORDER),
        "LIVE_TEMPLATE_INACTIVE_SEGMENT": attr(effect=DIM, effect_type=BORDER),
        "TEMPLATE_VARIABLE_ATTRIBUTES": attr(PINK),
        "INJECTED_LANGUAGE_FRAGMENT": attr(bg_="2E323D"),
        "HYPERLINK_ATTRIBUTES": attr(INFO, effect=INFO, effect_type=UNDERLINE),               # editorLink.activeForeground
        "FOLLOWED_HYPERLINK_ATTRIBUTES": attr(INFO, effect=INFO, effect_type=UNDERLINE),
        "INACTIVE_HYPERLINK_ATTRIBUTES": attr(DIM, effect=DIM, effect_type=UNDERLINE),
        "CTRL_CLICKABLE": attr(INFO, effect=INFO, effect_type=UNDERLINE),
        "DEFAULT_LINK": attr(INFO, effect=INFO, effect_type=UNDERLINE),
        "CUSTOM_KEYWORD1_ATTRIBUTES": attr(PURPLE, ft=I), "CUSTOM_KEYWORD2_ATTRIBUTES": attr(PINK),
        "CUSTOM_KEYWORD3_ATTRIBUTES": attr(HOTPINK), "CUSTOM_KEYWORD4_ATTRIBUTES": attr(BLUE),
        "IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES": attr(CYAN),
        "TABS": attr(bg_="333844"),
        "RAINBOW_COLOR0": attr(CYAN), "RAINBOW_COLOR1": attr(ORANGE), "RAINBOW_COLOR2": attr(YELLOW),
        "RAINBOW_COLOR3": attr(PINK), "RAINBOW_COLOR4": attr(BLUE),
        # ---- diff / vcs (diffEditor.*, merge.*) -------------------------------------------
        "DIFF_INSERTED": attr(bg_=B("29BF1220"), error_stripe=B("9BC53DBB")),
        "DIFF_DELETED": attr(bg_=B("F21B3F20"), error_stripe=B("FC644DBB")),
        "DIFF_MODIFIED": attr(bg_=B("5BC0EB20"), error_stripe=B("5BC0EBBB")),
        "DIFF_CONFLICT": attr(bg_=B("F9267240"), error_stripe="F92672"),                      # merge.currentContentBackground
        "VCS_ANNOTATIONS_COLOR_1": attr(),
        # ---- console / terminal (terminal.ansi*) ------------------------------------------
        "CONSOLE_NORMAL_OUTPUT": attr(FG), "CONSOLE_SYSTEM_OUTPUT": attr(FG), "CONSOLE_ERROR_OUTPUT": attr(RED),
        "CONSOLE_USER_INPUT": attr(GREEN, ft=I), "LOG_ERROR_OUTPUT": attr(RED), "LOG_WARNING_OUTPUT": attr(WARNING),
        "LOG_INFO_OUTPUT": attr(GREEN), "LOG_DEBUG_OUTPUT": attr(BLUE), "LOG_VERBOSE_OUTPUT": attr(DIM),
        "LOG_EXPIRED_ENTRY": attr(DIM),
        "CONSOLE_BLACK_OUTPUT": attr("000000"), "CONSOLE_DARKGRAY_OUTPUT": attr("666666"),
        "CONSOLE_GRAY_OUTPUT": attr("E5E5E5"), "CONSOLE_WHITE_OUTPUT": attr("FFFFFF"),
        "CONSOLE_RED_OUTPUT": attr(RED), "CONSOLE_RED_BRIGHT_OUTPUT": attr(RED),
        "CONSOLE_GREEN_OUTPUT": attr(GREEN), "CONSOLE_GREEN_BRIGHT_OUTPUT": attr(GREEN),
        "CONSOLE_YELLOW_OUTPUT": attr(YELLOW), "CONSOLE_YELLOW_BRIGHT_OUTPUT": attr(YELLOW),
        "CONSOLE_BLUE_OUTPUT": attr(BLUE), "CONSOLE_BLUE_BRIGHT_OUTPUT": attr(BLUE),
        "CONSOLE_MAGENTA_OUTPUT": attr(PINK), "CONSOLE_MAGENTA_BRIGHT_OUTPUT": attr(PINK),
        "CONSOLE_CYAN_OUTPUT": attr(CYAN), "CONSOLE_CYAN_BRIGHT_OUTPUT": attr(CYAN),
        "TERMINAL_COMMAND_TO_RUN_USING_IDE": attr(effect=CYAN, effect_type=UNDERLINE),
        "TERMINAL_CURSOR": attr("23262E", YELLOW),                                             # terminalCursor.*
        "BLOCK_TERMINAL_DEFAULT_FOREGROUND": attr(FG), "BLOCK_TERMINAL_DEFAULT_BACKGROUND": attr(bg_=bg),
        "BLOCK_TERMINAL_BLACK": attr("000000"), "BLOCK_TERMINAL_BLACK_BRIGHT": attr("666666"),
        "BLOCK_TERMINAL_WHITE": attr("E5E5E5"), "BLOCK_TERMINAL_WHITE_BRIGHT": attr("FFFFFF"),
        "BLOCK_TERMINAL_RED": attr(RED), "BLOCK_TERMINAL_RED_BRIGHT": attr(RED),
        "BLOCK_TERMINAL_GREEN": attr(GREEN), "BLOCK_TERMINAL_GREEN_BRIGHT": attr(GREEN),
        "BLOCK_TERMINAL_YELLOW": attr(YELLOW), "BLOCK_TERMINAL_YELLOW_BRIGHT": attr(YELLOW),
        "BLOCK_TERMINAL_BLUE": attr(BLUE), "BLOCK_TERMINAL_BLUE_BRIGHT": attr(BLUE),
        "BLOCK_TERMINAL_MAGENTA": attr(PINK), "BLOCK_TERMINAL_MAGENTA_BRIGHT": attr(PINK),
        "BLOCK_TERMINAL_CYAN": attr(CYAN), "BLOCK_TERMINAL_CYAN_BRIGHT": attr(CYAN),
        "BLOCK_TERMINAL_SELECTED_BLOCK_BACKGROUND": attr(bg_="2E323D"), "BLOCK_TERMINAL_SELECTED_BLOCK_STROKE_COLOR": attr(effect=DIM),
        "BLOCK_TERMINAL_INACTIVE_SELECTED_BLOCK_BACKGROUND": attr(bg_="282B35"), "BLOCK_TERMINAL_INACTIVE_SELECTED_BLOCK_STROKE_COLOR": attr(effect="333844"),
        "BLOCK_TERMINAL_HOVERED_BLOCK_BACKGROUND_START": attr(bg_="282B35"), "BLOCK_TERMINAL_HOVERED_BLOCK_BACKGROUND_END": attr(bg_="282B35"),
        "BLOCK_TERMINAL_BLOCK_BACKGROUND_START": attr(bg_=bg), "BLOCK_TERMINAL_BLOCK_BACKGROUND_END": attr(bg_=bg),
        "BLOCK_TERMINAL_ERROR_BLOCK_STROKE_COLOR": attr(effect=ERROR), "BLOCK_TERMINAL_PROMPT_SEPARATOR_COLOR": attr(effect="333844"),
        "BLOCK_TERMINAL_CURRENT_SEARCH_ENTRY": attr(bg_=B("F39D1256")),
        "BLOCK_TERMINAL_GENERATE_COMMAND_CARET_COLOR": attr(effect="FFFFFF"), "BLOCK_TERMINAL_GENERATE_COMMAND_PLACEHOLDER_FOREGROUND": attr(DIM),
        "BLOCK_TERMINAL_GENERATE_COMMAND_PROMPT_TEXT": attr(FG),
        "BLOCK_TERMINAL_SELECTED_BLOCK": attr(bg_="2E323D"),
        "BLOCK_TERMINAL_SEARCH_ENTRY": attr(bg_=B("59B8B377")),
        "BLOCK_TERMINAL_SEARCH_ENTRY_CURRENT": attr(bg_=B("F39D1256")),
        "BLOCK_TERMINAL_COMMAND": attr(FG), "BLOCK_TERMINAL_PROMPT": attr(CYAN),
        "BLOCK_TERMINAL_HOVERED_BLOCK": attr(bg_="282B35"), "BLOCK_TERMINAL_INACTIVE_SELECTED_BLOCK": attr(bg_="282B35"),
        "BLOCK_TERMINAL_ERROR_BLOCK": attr(bg_=B("F21B3F20")),
        # ---- breadcrumbs / sticky lines ---------------------------------------------------
        "BREADCRUMBS_DEFAULT": attr(DIM), "BREADCRUMBS_HOVERED": attr(FG), "BREADCRUMBS_CURRENT": attr(CYAN),
        "BREADCRUMBS_INACTIVE": attr(DIM),
        # ---- language specifics (scopes noted) --------------------------------------------
        # Java / Kotlin
        "ANNOTATION_NAME_ATTRIBUTES": attr(PURPLE), "ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES": attr(YELLOW),
        "CONSTRUCTOR_CALL_ATTRIBUTES": attr(YELLOW), "CONSTRUCTOR_DECLARATION_ATTRIBUTES": attr(YELLOW),
        "STATIC_FINAL_FIELD_ATTRIBUTES": attr(RED), "STATIC_FIELD_ATTRIBUTES": attr(ORANGE),
        "STATIC_METHOD_ATTRIBUTES": attr(YELLOW), "INSTANCE_FIELD_ATTRIBUTES": attr(ORANGE),
        "TYPE_PARAMETER_NAME_ATTRIBUTES": attr(YELLOW), "ABSTRACT_CLASS_NAME_ATTRIBUTES": attr(YELLOW),
        "ANONYMOUS_CLASS_NAME_ATTRIBUTES": attr(YELLOW), "ENUM_NAME_ATTRIBUTES": attr(YELLOW),
        "INTERFACE_NAME_ATTRIBUTES": attr(YELLOW), "RECORD_NAME_ATTRIBUTES": attr(YELLOW),
        "CLASS_NAME_ATTRIBUTES": attr(YELLOW), "CLASS_REFERENCE_ATTRIBUTES": attr(YELLOW),
        "LOCAL_VARIABLE_ATTRIBUTES": attr(CYAN), "PARAMETER_ATTRIBUTES": attr(CYAN),
        "REASSIGNED_LOCAL_VARIABLE_ATTRIBUTES": attr(CYAN, effect=DIM, effect_type=UNDERLINE),
        "REASSIGNED_PARAMETER_ATTRIBUTES": attr(CYAN, effect=DIM, effect_type=UNDERLINE),
        "IMPLICIT_ANONYMOUS_CLASS_PARAMETER": attr(CYAN),
        "METHOD_CALL_ATTRIBUTES": attr(YELLOW), "METHOD_DECLARATION_ATTRIBUTES": attr(YELLOW),
        "ABSTRACT_METHOD_ATTRIBUTES": attr(YELLOW), "INHERITED_METHOD_ATTRIBUTES": attr(YELLOW),
        "JAVA_KEYWORD": attr(PURPLE, ft=I), "JAVA_NUMBER": attr(ORANGE), "JAVA_STRING": attr(GREEN),
        "JAVA_OPERATION_SIGN": attr(RED), "JAVA_LINE_COMMENT": attr(COMMENT, ft=I), "JAVA_BLOCK_COMMENT": attr(COMMENT, ft=I),
        "JAVA_DOC_COMMENT": attr(COMMENT, ft=I), "JAVA_DOC_TAG": attr(COMMENT, ft=I | 1), "JAVA_DOC_MARKUP": attr(COMMENT, ft=I),
        "JAVA_VALID_STRING_ESCAPE": attr(GREEN), "JAVA_INVALID_STRING_ESCAPE": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        "JAVA_BRACES": attr(FG), "JAVA_BRACKETS": attr(FG), "JAVA_PARENTH": attr(FG), "JAVA_COMMA": attr(FG),
        "JAVA_SEMICOLON": attr(FG), "JAVA_DOT": attr(FG),
        "KOTLIN_NAMED_ARGUMENT": attr(CYAN), "KOTLIN_LABEL": attr(FG), "KOTLIN_SMART_CAST_VALUE": attr(bg_="2E323D"),
        "KOTLIN_MUTABLE_VARIABLE": attr(CYAN, effect=DIM, effect_type=UNDERLINE), "KOTLIN_WRAPPED_INTO_REF": attr(CYAN, effect=DIM, effect_type=UNDERLINE),
        "KOTLIN_EXTENSION_PROPERTY": attr(ORANGE), "KOTLIN_BACKING_FIELD_VARIABLE": attr(ORANGE),
        "KOTLIN_SMART_CONSTANT": attr(RED), "KOTLIN_ENUM_ENTRY": attr(RED), "KOTLIN_OBJECT": attr(YELLOW),
        "KOTLIN_TYPE_ALIAS": attr(YELLOW), "KOTLIN_TYPE_PARAMETER": attr(YELLOW), "KOTLIN_TRAIT": attr(YELLOW),
        "KOTLIN_BUILTIN_ANNOTATION": attr(PURPLE), "KOTLIN_ANNOTATION": attr(PURPLE),
        "KOTLIN_DYNAMIC_FUNCTION_CALL": attr(YELLOW), "KOTLIN_PACKAGE_FUNCTION_CALL": attr(YELLOW),
        "KOTLIN_EXTENSION_FUNCTION_CALL": attr(YELLOW), "KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW": attr(FG, ft=1),
        "KOTLIN_INSTANCE_PROPERTY": attr(ORANGE), "KOTLIN_CLASS_OBJECT_FUNCTION_CALL": attr(YELLOW),
        "KOTLIN_SUSPEND_FUNCTION_CALL": attr(YELLOW), "KOTLIN_INSTANCE_PROPERTY_CUSTOM_PROPERTY_DECLARATION": attr(ORANGE),
        "KOTLIN_PROPERTY_WITH_BACKING_FIELD": attr(ORANGE), "KOTLIN_PACKAGE_PROPERTY": attr(ORANGE),
        "KOTLIN_PACKAGE_PROPERTY_CUSTOM_PROPERTY_DECLARATION": attr(ORANGE),
        "KOTLIN_DYNAMIC_PROPERTY_CALL": attr(ORANGE), "KOTLIN_ANDROID_EXTENSIONS_PROPERTY_CALL": attr(ORANGE),
        "KOTLIN_KEYWORD": attr(PURPLE, ft=I), "KOTLIN_BUILTIN_KEYWORD": attr(PURPLE, ft=I),
        "KOTLIN_VARIABLE_AS_FUNCTION_CALL": attr(YELLOW), "KOTLIN_VARIABLE_AS_FUNCTION_LIKE_CALL": attr(YELLOW),
        "KOTLIN_NAMED_ARGUMENT_AS_KEYWORD": attr(CYAN),
        "KOTLIN_CLASS": attr(YELLOW), "KOTLIN_DATA_CLASS": attr(YELLOW), "KOTLIN_DATA_OBJECT": attr(YELLOW), "KOTLIN_ENUM": attr(YELLOW),
        "KOTLIN_ABSTRACT_CLASS": attr(YELLOW), "KOTLIN_CONSTRUCTOR": attr(YELLOW), "KOTLIN_FUNCTION_CALL": attr(YELLOW),
        "KOTLIN_FUNCTION_DECLARATION": attr(YELLOW), "KOTLIN_PARAMETER": attr(CYAN), "KOTLIN_LOCAL_VARIABLE": attr(CYAN),
        "KOTLIN_KEYWORD_VAL": attr(PURPLE, ft=I), "KOTLIN_KEYWORD_VAR": attr(PURPLE, ft=I), "KOTLIN_STRING": attr(GREEN),
        "KOTLIN_STRING_ESCAPE": attr(GREEN), "KOTLIN_INVALID_STRING_ESCAPE": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        "KOTLIN_NUMBER": attr(ORANGE), "KOTLIN_OPERATION_SIGN": attr(RED), "KOTLIN_ARROW": attr(PURPLE), "KOTLIN_DOUBLE_COLON": attr(RED),
        "KOTLIN_SAFE_ACCESS": attr(RED), "KOTLIN_EXCLEXCL": attr(RED), "KOTLIN_QUEST": attr(RED), "KOTLIN_AMPERSAND": attr(RED),
        "KOTLIN_LINE_COMMENT": attr(COMMENT, ft=I), "KOTLIN_BLOCK_COMMENT": attr(COMMENT, ft=I), "KOTLIN_DOC_COMMENT": attr(COMMENT, ft=I),
        "KOTLIN_ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES": attr(YELLOW), "KOTLIN_CONTEXT_ARGUMENT": attr(CYAN),
        "KOTLIN_SYNTHETIC_EXTENSION_PROPERTY": attr(ORANGE), "KOTLIN_VARIABLE_AS_FUNCTION": attr(YELLOW), "KOTLIN_VARIABLE_AS_FUNCTION_LIKE": attr(YELLOW),
        "KOTLIN_CLOSURE_DEFAULT_PARAMETER": attr(CYAN), "KOTLIN_SMART_CAST_RECEIVER": attr(bg_="2E323D"),
        "KOTLIN_BRACES": attr(FG), "KOTLIN_BRACKETS": attr(FG), "KOTLIN_PARENTHESIS": attr(FG), "KOTLIN_COMMA": attr(FG),
        "KOTLIN_SEMICOLON": attr(FG), "KOTLIN_DOT": attr(FG), "KOTLIN_COLON": attr(FG),
        # JavaScript / TypeScript
        "JS.GLOBAL_VARIABLE": attr(CYAN), "JS.LOCAL_VARIABLE": attr(CYAN), "JS.PARAMETER": attr(CYAN),
        "JS.GLOBAL_FUNCTION": attr(YELLOW), "JS.LOCAL_FUNCTION": attr(YELLOW),
        "JS.INSTANCE_MEMBER_FUNCTION": attr(YELLOW), "JS.STATIC_MEMBER_FUNCTION": attr(YELLOW),
        "JS.INSTANCE_MEMBER_VARIABLE": attr(ORANGE), "JS.STATIC_MEMBER_VARIABLE": attr(ORANGE),
        "JS.CLASS": attr(YELLOW), "JS.INTERFACE": attr(YELLOW), "JS.TYPE_ALIAS": attr(YELLOW),
        "JS.PRIMITIVE.TYPE": attr(PURPLE),                                                         # support.type -> Purple
        "JS.DECORATOR": attr(YELLOW), "JS.REGEXP": attr(BLUE),                                     # string.regexp -> Blue
        "JS.KEYWORD": attr(PURPLE, ft=I), "JS.NUMBER": attr(ORANGE), "JS.STRING": attr(GREEN),
        "JS.OPERATION_SIGN": attr(RED), "JS.LINE_COMMENT": attr(COMMENT, ft=I), "JS.BLOCK_COMMENT": attr(COMMENT, ft=I),
        "JS.DOC_COMMENT": attr(COMMENT, ft=I), "JS.DOC_TAG": attr(COMMENT, ft=I | 1),
        "JS.MODULE_NAME": attr(CYAN), "JS.LABEL": attr(FG), "JS.EXPORTED_FUNCTION": attr(YELLOW),
        "JS.TEMPLATE_LITERAL_PLACEHOLDER_DELIMITERS": attr(HOTPINK),                               # punctuation.definition.template-expression -> Hot Pink
        "JS.FUNCTION_ARROW": attr(PURPLE),                                                         # storage.type.function.arrow -> Purple
        "JS.EXPORTED.VARIABLE": attr(CYAN), "JS.EXPORTED.FUNCTION": attr(YELLOW), "JS.EXPORTED.CLASS": attr(YELLOW),
        "JS.DOC_TYPE": attr(YELLOW, ft=I), "JS.DOC_TAG_NAMEPATH": attr(CYAN, ft=I), "JS.EXCEPTION": attr(YELLOW),
        "JS.JSX_CLIENT_COMPONENT": attr(YELLOW), "JS.VALUE_HINT": attr(DIM),
        "JavaScript:INJECTED_LANGUAGE_FRAGMENT": attr(bg_=bg),
        "JS.BRACES": attr(FG), "JS.BRACKETS": attr(FG), "JS.PARENTHS": attr(FG), "JS.COMMA": attr(FG),
        "JS.SEMICOLON": attr(FG), "JS.DOT": attr(FG), "JS.BADCHARACTER": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        "JS.VALID_STRING_ESCAPE": attr(GREEN), "JS.INVALID_STRING_ESCAPE": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        # TypeScript mirrors JS
        "TS.GLOBAL_VARIABLE": attr(CYAN), "TS.LOCAL_VARIABLE": attr(CYAN), "TS.PARAMETER": attr(CYAN),
        "TS.GLOBAL_FUNCTION": attr(YELLOW), "TS.LOCAL_FUNCTION": attr(YELLOW),
        "TS.INSTANCE_MEMBER_FUNCTION": attr(YELLOW), "TS.STATIC_MEMBER_FUNCTION": attr(YELLOW),
        "TS.INSTANCE_MEMBER_VARIABLE": attr(ORANGE), "TS.STATIC_MEMBER_VARIABLE": attr(ORANGE),
        "TS.CLASS": attr(YELLOW), "TS.INTERFACE": attr(YELLOW), "TS.TYPE.ALIAS": attr(YELLOW), "TS.TYPE_PARAMETER": attr(YELLOW),
        "TS.PRIMITIVE.TYPES": attr(PURPLE), "TS.TYPE_GUARD": attr(PURPLE), "TS.DECORATOR": attr(YELLOW), "TS.REGEXP": attr(BLUE),
        "TS.KEYWORD": attr(PURPLE, ft=I), "TS.NUMBER": attr(ORANGE), "TS.STRING": attr(GREEN), "TS.OPERATION_SIGN": attr(RED),
        "TS.LINE_COMMENT": attr(COMMENT, ft=I), "TS.BLOCK_COMMENT": attr(COMMENT, ft=I), "TS.DOC_COMMENT": attr(COMMENT, ft=I),
        "TS.DOC_TAG": attr(COMMENT, ft=I | 1), "TS.DOC_TYPE": attr(YELLOW, ft=I), "TS.DOC_TAG_NAMEPATH": attr(CYAN, ft=I),
        "TS.LABEL": attr(FG), "TS.FUNCTION_ARROW": attr(PURPLE),
        "TS.EXPORTED.VARIABLE": attr(CYAN), "TS.EXPORTED.FUNCTION": attr(YELLOW), "TS.EXPORTED.CLASS": attr(YELLOW),
        "TS.BRACES": attr(FG), "TS.BRACKETS": attr(FG), "TS.PARENTHS": attr(FG), "TS.COMMA": attr(FG), "TS.SEMICOLON": attr(FG), "TS.DOT": attr(FG),
        "TS.VALID_STRING_ESCAPE": attr(GREEN), "TS.INVALID_STRING_ESCAPE": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        "TS.BADCHARACTER": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        # Python
        "PY.KEYWORD": attr(PURPLE, ft=I), "PY.NUMBER": attr(ORANGE), "PY.STRING": attr(GREEN),
        "PY.STRING.B": attr(GREEN), "PY.STRING.U": attr(GREEN), "PY.OPERATION_SIGN": attr(RED),
        "PY.LINE_COMMENT": attr(COMMENT, ft=I), "PY.DOC_COMMENT": attr(COMMENT, ft=I), "PY.DOC_COMMENT_TAG": attr(COMMENT, ft=I | 1),
        "PY.SELF_PARAMETER": attr(PINK),                                                           # variable.language.special.self -> Pink
        "PY.BUILTIN_NAME": attr(YELLOW),                                                           # support.function -> Yellow
        "PY.PREDEFINED_USAGE": attr(YELLOW), "PY.PREDEFINED_DEFINITION": attr(YELLOW),
        "PY.DECORATOR": attr(YELLOW), "PY.FUNC_DEFINITION": attr(YELLOW), "PY.CLASS_DEFINITION": attr(YELLOW),
        "PY.FUNCTION_CALL": attr(YELLOW), "PY.METHOD_CALL": attr(YELLOW),
        "PY.KEYWORD_ARGUMENT": attr(CYAN), "PY.PARAMETER": attr(CYAN), "PY.LOCAL_VARIABLE": attr(CYAN),
        "PY.NONLOCAL": attr(CYAN), "PY.ANNOTATION": attr(YELLOW), "PY.TYPE_ANNOTATION": attr(YELLOW),
        "PY.ANNOTATION.CLASS_NAME": attr(YELLOW), "PY.CLASS_REFERENCE": attr(YELLOW),
        "PY.FSTRING_FRAGMENT_BRACES": attr(HOTPINK), "PY.FSTRING.TEXT": attr(GREEN),
        "PY.VALID_STRING_ESCAPE": attr(GREEN), "PY.INVALID_STRING_ESCAPE": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        "PY.BRACES": attr(FG), "PY.BRACKETS": attr(FG), "PY.PARENTHS": attr(FG), "PY.COMMA": attr(FG), "PY.DOT": attr(FG),
        # Go
        "GO_KEYWORD": attr(PURPLE, ft=I), "GO_BUILTIN_TYPE_REFERENCE": attr(PURPLE), "GO_BUILTIN_FUNCTION_CALL": attr(YELLOW),
        "GO_BUILTIN_CONSTANT": attr(RED), "GO_BUILTIN_VARIABLE": attr(CYAN), "GO_PACKAGE": attr(CYAN),
        "GO_PACKAGE_LOCAL_FUNCTION_CALL": attr(YELLOW), "GO_PACKAGE_EXPORTED_FUNCTION_CALL": attr(YELLOW),
        "GO_PACKAGE_LOCAL_FUNCTION": attr(YELLOW), "GO_PACKAGE_EXPORTED_FUNCTION": attr(YELLOW),
        "GO_STRUCT_EXPORTED_MEMBER": attr(ORANGE), "GO_STRUCT_LOCAL_MEMBER": attr(ORANGE),
        "GO_STRUCT_EXPORTED_METHOD": attr(YELLOW), "GO_STRUCT_LOCAL_METHOD": attr(YELLOW),
        "GO_STRUCT_EXPORTED_METHOD_CALL": attr(YELLOW), "GO_STRUCT_LOCAL_METHOD_CALL": attr(YELLOW),
        "GO_TYPE_REFERENCE": attr(YELLOW), "GO_TYPE_SPECIFICATION": attr(YELLOW), "GO_TYPE_PARAMETER": attr(YELLOW),
        "GO_STRUCT_TAG": attr(GREEN), "GO_STRING": attr(GREEN), "GO_NUMBER": attr(ORANGE), "GO_OPERATOR": attr(RED),
        "GO_LINE_COMMENT": attr(COMMENT, ft=I), "GO_BLOCK_COMMENT": attr(COMMENT, ft=I), "GO_COMMENT_REFERENCE": attr(COMMENT, ft=I | 1),
        "GO_LOCAL_VARIABLE": attr(CYAN), "GO_FUNCTION_PARAMETER": attr(CYAN), "GO_METHOD_RECEIVER": attr(CYAN),
        "GO_PACKAGE_EXPORTED_VARIABLE": attr(CYAN), "GO_PACKAGE_LOCAL_VARIABLE": attr(CYAN),
        "GO_PACKAGE_EXPORTED_CONSTANT": attr(RED), "GO_PACKAGE_LOCAL_CONSTANT": attr(RED), "GO_LOCAL_CONSTANT": attr(RED),
        "GO_SHADOWING_VARIABLE": attr(CYAN, effect=DIM, effect_type=UNDERLINE), "GO_LABEL": attr(FG),
        "GO_DIRECTIVE_COMMENT": attr(COMMENT, ft=I | 1),
        # CSS / SCSS / LESS
        "CSS.TAG_NAME": attr(HOTPINK),                                                             # entity.name.tag -> Hot Pink
        "CSS.CLASS_NAME": attr(YELLOW),                                                            # source.css entity.other.attribute-name -> Yellow
        "CSS.HASH": attr(RED),                                                                     # entity.other.attribute-name.id (#id) -> Red
        "CSS.AMPERSAND": attr(CYAN),                                                               # parent-selector (&) -> Cyan
        "CSS.ATTRIBUTE_NAME": attr(YELLOW), "CSS.PSEUDO": attr(YELLOW),
        "CSS.PROPERTY_NAME": attr(PURPLE),                                                         # support.type.property-name -> Purple
        "CSS.PROPERTY_VALUE": attr(FG), "CSS.KEYWORD": attr(PURPLE, ft=I), "CSS.IMPORTANT": attr(PURPLE),
        "CSS.NUMBER": attr(ORANGE), "CSS.UNIT": attr(ORANGE),                                       # keyword.other.unit -> Orange
        "CSS.FUNCTION": attr(RED),                                                                 # source.css support.function -> Red
        "CSS.COLOR": attr(RED),                                                                    # constant.other.color -> Red
        "CSS.STRING": attr(GREEN), "CSS.URL": attr(GREEN), "CSS.COMMENT": attr(COMMENT, ft=I),
        "CSS.IDENT": attr(FG), "CSS.OPERATORS": attr(RED), "CSS.BRACES": attr(FG), "CSS.BRACKETS": attr(FG),
        "CSS.PARENTHESES": attr(FG), "CSS.COMMA": attr(FG), "CSS.DOT": attr(FG), "CSS.SEMICOLON": attr(FG), "CSS.COLON": attr(FG),
        "CSS.AT_RULE": attr(PURPLE), "CSS.CUSTOM_PROPERTY": attr(CYAN), "CSS.CUSTOM_PROPERTY_REFERENCE": attr(CYAN),
        "CSS.UNICODE.RANGE": attr(ORANGE), "CSS.BAD_CHARACTER": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        "SASS_VARIABLE": attr(CYAN), "SASS_MIXIN": attr(YELLOW), "SASS_FUNCTION": attr(YELLOW), "SASS_KEYWORD": attr(PURPLE),
        "SASS_PLACEHOLDER": attr(YELLOW), "SASS_INTERPOLATION": attr(HOTPINK),
        "LESS_VARIABLE": attr(CYAN), "LESS_MIXIN": attr(YELLOW), "LESS_JS_CODE_DELIM": attr(HOTPINK), "LESS_INJECTED_CODE": attr(FG),
        # HTML / XML
        "HTML_TAG": attr(FG), "HTML_TAG_NAME": attr(HOTPINK), "HTML_CUSTOM_TAG_NAME": attr(HOTPINK),
        "HTML_ATTRIBUTE_NAME": attr(YELLOW, ft=I), "HTML_ATTRIBUTE_VALUE": attr(GREEN), "HTML_ENTITY_REFERENCE": attr(CYAN),
        "HTML_COMMENT": attr(COMMENT, ft=I), "HTML_CODE": attr(FG),
        "XML_TAG": attr(FG), "XML_TAG_NAME": attr(HOTPINK), "XML_CUSTOM_TAG_NAME": attr(HOTPINK), "XML_NS_PREFIX": attr(HOTPINK),
        "XML_ATTRIBUTE_NAME": attr(YELLOW, ft=I), "XML_ATTRIBUTE_VALUE": attr(YELLOW),            # text.xml string -> Yellow
        "XML_ENTITY_REFERENCE": attr(CYAN), "XML_COMMENT": attr(COMMENT, ft=I), "XML_PROLOGUE": attr(PURPLE),
        "XML_TAG_DATA": attr(FG), "XML_INJECTED_LANGUAGE_FRAGMENT": attr(bg_=bg), "XML_PROCESSING_INSTRUCTION": attr(PURPLE),
        # Markdown (markup.*)
        "MARKDOWN_HEADER_LEVEL_1": attr(PINK, ft=1), "MARKDOWN_HEADER_LEVEL_2": attr(PINK, ft=1), "MARKDOWN_HEADER_LEVEL_3": attr(PINK, ft=1),
        "MARKDOWN_HEADER_LEVEL_4": attr(PINK, ft=1), "MARKDOWN_HEADER_LEVEL_5": attr(PINK, ft=1), "MARKDOWN_HEADER_LEVEL_6": attr(PINK, ft=1),
        "MARKDOWN_BOLD": attr(ORANGE, ft=1), "MARKDOWN_ITALIC": attr(PURPLE, ft=2), "MARKDOWN_BOLD_ITALIC": attr(ORANGE, ft=3),
        "MARKDOWN_STRIKE_THROUGH": attr(RED, effect=RED, effect_type=STRIKE),
        "MARKDOWN_CODE_SPAN": attr(GREEN), "MARKDOWN_CODE_BLOCK": attr(FG), "MARKDOWN_CODE_FENCE": attr(FG),
        "MARKDOWN_LIST_MARKER": attr(YELLOW), "MARKDOWN_LIST_ITEM": attr(FG), "MARKDOWN_UNORDERED_LIST": attr(FG), "MARKDOWN_ORDERED_LIST": attr(FG),
        "MARKDOWN_BLOCK_QUOTE": attr(COMMENT, ft=I), "MARKDOWN_BLOCK_QUOTE_MARKER": attr(COMMENT),
        "MARKDOWN_LINK_TEXT": attr(PURPLE), "MARKDOWN_LINK_DESTINATION": attr(GREEN), "MARKDOWN_LINK_LABEL": attr(PURPLE),
        "MARKDOWN_LINK_TITLE": attr(GREEN), "MARKDOWN_LINK_DEFINITION": attr(PURPLE), "MARKDOWN_EXPLICIT_LINK": attr(PURPLE),
        "MARKDOWN_AUTO_LINK": attr(PURPLE), "MARKDOWN_REFERENCE_LINK": attr(PURPLE), "MARKDOWN_IMAGE": attr(PURPLE),
        "MARKDOWN_HTML_BLOCK": attr(FG), "MARKDOWN_INLINE_HTML": attr(HOTPINK), "MARKDOWN_HRULE": attr(DIM),
        "MARKDOWN_TABLE_SEPARATOR": attr(DIM), "MARKDOWN_TEXT": attr(FG), "MARKDOWN_COMMENT": attr(COMMENT, ft=I),
        "MARKDOWN_DEFINITION_LIST": attr(FG), "MARKDOWN_HEADER": attr(PINK, ft=1), "MARKDOWN_HEADER_BOLD": attr(PINK, ft=1),
        "MARKDOWN_HEADER_MARKER": attr(PINK, ft=1), "MARKDOWN_BOLD_MARKER": attr(ORANGE), "MARKDOWN_ITALIC_MARKER": attr(PURPLE),
        "MARKDOWN_CODE_SPAN_MARKER": attr(GREEN), "MARKDOWN_CODE_FENCE_MARKER": attr(FG),
        "MARKDOWN_CODE_FENCE_LANGUAGE": attr(ORANGE),                                              # fenced_code.block.language -> Orange
        "MARKDOWN_TERM": attr(YELLOW), "MARKDOWN_DEFINITION": attr(FG), "MARKDOWN_DEFINITION_LIST_MARKER": attr(YELLOW),
        "MARKDOWN_FOOTNOTE_DEFINITION": attr(PURPLE), "MARKDOWN_FRONT_MATTER_HEADER_DELIMITER": attr(DIM),
        "MARKDOWN_ALERT_TITLE_NOTE": attr(INFO, ft=1), "MARKDOWN_ALERT_TITLE_TIP": attr(GREEN, ft=1), "MARKDOWN_ALERT_TITLE_IMPORTANT": attr(PURPLE, ft=1),
        "MARKDOWN_ALERT_TITLE_WARNING": attr(WARNING, ft=1), "MARKDOWN_ALERT_TITLE_CAUTION": attr(ERROR, ft=1),
        # YAML / JSON / TOML / properties
        "YAML_SCALAR_KEY": attr(CYAN),                                                             # entity.name.tag.yaml -> Cyan
        "YAML_SCALAR_VALUE": attr(GREEN), "YAML_SCALAR_STRING": attr(GREEN), "YAML_SCALAR_DSTRING": attr(GREEN),
        "YAML_SCALAR_LIST": attr(GREEN), "YAML_SCALAR_TEXT": attr(GREEN), "YAML_ANCHOR": attr(PINK), "YAML_ALIAS": attr(PINK),
        "YAML_COMMENT": attr(COMMENT, ft=I), "YAML_SIGN": attr(FG), "YAML_TEXT": attr(FG),
        "JSON.PROPERTY_KEY": attr(CYAN),                                                           # support.type.property-name.json -> Cyan
        "JSON.STRING": attr(GREEN), "JSON.NUMBER": attr(ORANGE), "JSON.KEYWORD": attr(RED),        # constant.language -> Red
        "JSON.LINE_COMMENT": attr(COMMENT, ft=I), "JSON.BLOCK_COMMENT": attr(COMMENT, ft=I),
        "JSON.BRACES": attr(FG), "JSON.BRACKETS": attr(FG), "JSON.COMMA": attr(FG), "JSON.COLON": attr(FG),
        "JSON.PARAMETER": attr(PINK),
        "TOML_KEY": attr(CYAN), "TOML_STRING": attr(GREEN), "TOML_NUMBER": attr(ORANGE), "TOML_BOOLEAN": attr(RED),
        "TOML_DATE": attr(ORANGE), "TOML_COMMENT": attr(COMMENT, ft=I),
        "PROPERTIES_KEY": attr(CYAN), "PROPERTIES_VALUE": attr(GREEN), "PROPERTIES_COMMENT": attr(COMMENT, ft=I),
        "PROPERTIES_KEY_VALUE_SEPARATOR": attr(FG), "PROPERTIES_VALID_STRING_ESCAPE": attr(GREEN),
        "PROPERTIES_INVALID_STRING_ESCAPE": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE),
        # Shell / Dockerfile / Regex / SQL / PHP / Ruby (main scopes)
        "BASH.KEYWORD": attr(PURPLE, ft=I), "BASH.SHEBANG": attr(COMMENT, ft=I), "BASH.LINE_COMMENT": attr(COMMENT, ft=I),
        "BASH.STRING": attr(GREEN), "BASH.RAW_STRING": attr(GREEN), "BASH.HERE_DOC": attr(GREEN), "BASH.NUMBER": attr(ORANGE),
        "BASH.VAR_USE": attr(CYAN), "BASH.VAR_DEF": attr(CYAN), "BASH.VAR_USE_BUILTIN": attr(CYAN),
        "BASH.FUNCTION_DEF_NAME": attr(YELLOW), "BASH.EXTERNAL_COMMAND": attr(YELLOW), "BASH.SUBSHELL_COMMAND": attr(YELLOW),
        "BASH.CONDITIONAL": attr(FG), "BASH.REDIRECTION": attr(RED), "BASH.HERE_DOC_START": attr(PURPLE), "BASH.HERE_DOC_END": attr(PURPLE),
        "BASH.GENERIC_COMMAND": attr(YELLOW), "BASH.FUNCTION_CALL": attr(YELLOW), "BASH.BRACES": attr(FG), "BASH.BRACKETS": attr(FG),
        "BASH.PARENTHESES": attr(FG), "BASH.BACKQUOTE": attr(HOTPINK), "BASH.STRING2": attr(GREEN), "BASH.INTERNAL_COMMAND": attr(YELLOW),
        "DOCKERFILE_KEYWORD": attr(PURPLE, ft=I), "DOCKERFILE_STRING": attr(GREEN), "DOCKERFILE_COMMENT": attr(COMMENT, ft=I),
        "REGEXP.META": attr(BLUE), "REGEXP.CHARACTER": attr(BLUE), "REGEXP.QUANTIFIER": attr(BLUE), "REGEXP.BRACKETS": attr(BLUE),
        "REGEXP.BRACES": attr(BLUE), "REGEXP.PARENTHS": attr(BLUE), "REGEXP.ESC_CHARACTER": attr(BLUE), "REGEXP.CHAR_CLASS": attr(BLUE),
        "REGEXP.INVALID_STRING_ESCAPE": attr(ERROR, effect=ERROR, effect_type=UNDERWAVE), "REGEXP.REDUNDANT_ESCAPE": attr(BLUE),
        "REGEXP.NAME": attr(BLUE), "REGEXP.COMMENT": attr(COMMENT, ft=I), "REGEXP.OPTIONS": attr(BLUE), "REGEXP.MATCHED_GROUPS": attr(bg_="2E323D"),
        "SQL_KEYWORD": attr(PURPLE, ft=I), "SQL_STRING": attr(GREEN), "SQL_NUMBER": attr(ORANGE), "SQL_COMMENT": attr(COMMENT, ft=I),
        "SQL_LINE_COMMENT": attr(COMMENT, ft=I), "SQL_BLOCK_COMMENT": attr(COMMENT, ft=I), "SQL_TABLE": attr(YELLOW), "SQL_COLUMN": attr(CYAN),
        "SQL_SCHEMA": attr(YELLOW), "SQL_PROCEDURE": attr(YELLOW), "SQL_ALIAS": attr(CYAN), "SQL_PARAMETER": attr(CYAN),
        "SQL_LOCAL_VARIABLE": attr(CYAN), "SQL_LOCAL_ALIAS": attr(CYAN), "SQL_DATABASE_OBJECT": attr(YELLOW), "SQL_SYNTHETIC_ENTITY": attr(YELLOW),
        "SQL_OUTER_QUERY_COLUMN": attr(CYAN), "SQL_TYPE": attr(PURPLE), "SQL_IDENT": attr(FG), "SQL_IDENT_DELIMITED": attr(FG),
        "PHP_KEYWORD": attr(PURPLE, ft=I), "PHP_VAR": attr(CYAN), "PHP_THIS_VAR": attr(PINK), "PHP_STRING": attr(GREEN),
        "PHP_NUMBER": attr(ORANGE), "PHP_CONSTANT": attr(ORANGE),                                  # constant.other.php -> Orange
        "PHP_FUNCTION_CALL": attr(YELLOW), "PHP_FUNCTION_DECLARATION": attr(YELLOW), "PHP_METHOD_CALL": attr(YELLOW),
        "PHP_PREDEFINED_SYMBOL": attr(RED),                                                        # source.php support.function -> Red
        "PHP_CLASS": attr(YELLOW), "PHP_INTERFACE": attr(YELLOW), "PHP_TRAIT": attr(YELLOW), "PHP_NAMESPACE": attr(CYAN),
        "PHP_COMMENT": attr(COMMENT, ft=I), "PHP_DOC_COMMENT": attr(COMMENT, ft=I), "PHP_DOC_TAG": attr(COMMENT, ft=I | 1),
        "PHP_EXEC_COMMAND": attr(GREEN), "PHP_HEREDOC_CONTENT": attr(GREEN), "PHP_HEREDOC_ID": attr(PURPLE),
        "PHP_OPENING_TAG": attr(HOTPINK), "PHP_CLOSING_TAG": attr(HOTPINK),                        # punctuation.section.embedded.*.php -> Hot Pink
        "PHP_PARAMETER": attr(CYAN), "PHP_STATIC_MEMBER_FUNCTION": attr(YELLOW), "PHP_INSTANCE_MEMBER_VARIABLE": attr(ORANGE),
        "RUBY_KEYWORD": attr(PURPLE, ft=I), "RUBY_STRING": attr(GREEN), "RUBY_NUMBER": attr(ORANGE), "RUBY_COMMENT": attr(COMMENT, ft=I),
        "RUBY_IDENTIFIER": attr(CYAN), "RUBY_CONSTANT": attr(RED), "RUBY_METHOD_NAME": attr(YELLOW), "RUBY_SYMBOL": attr(ORANGE),
        "RUBY_IVAR": attr(ORANGE), "RUBY_GVAR": attr(CYAN), "RUBY_CVAR": attr(ORANGE), "RUBY_REGEXP": attr(BLUE),
        "RUBY_EXPR_IN_STRING_SUBST": attr(HOTPINK), "RUBY_EXPR_SUBST_MARKS": attr(HOTPINK),          # punctuation.section.embedded.*.ruby -> Hot Pink
        "RUBY_HEREDOC_ID": attr(PURPLE), "RUBY_HEREDOC_CONTENT": attr(GREEN), "RUBY_ESCAPE_SEQUENCE": attr(GREEN),
        "RUBY_NTH_REF": attr(CYAN), "RUBY_BACK_REF": attr(CYAN), "RUBY_PARAMDEF_CALL": attr(YELLOW), "RUBY_PARAMETER_ID": attr(CYAN),
        "RUBY_SPECIFIC_CALL": attr(YELLOW), "RUBY_METHOD_DEFINITION": attr(YELLOW), "RUBY_CLASS_DEFINITION": attr(YELLOW),
        # C/C++/Rust minimal
        "RUST_KEYWORD": attr(PURPLE, ft=I), "RUST_MACRO": attr(YELLOW), "RUST_LIFETIME": attr(HOTPINK), "RUST_ATTRIBUTE": attr(PURPLE),
        "RUST_SELF_PARAMETER": attr(PINK), "RUST_FUNCTION": attr(YELLOW), "RUST_METHOD": attr(YELLOW), "RUST_STRUCT": attr(YELLOW),
        "RUST_TRAIT": attr(YELLOW), "RUST_ENUM": attr(YELLOW), "RUST_ENUM_VARIANT": attr(RED), "RUST_CONST": attr(RED), "RUST_STATIC": attr(RED),
        "RUST_FIELD": attr(ORANGE), "RUST_TYPE_PARAMETER": attr(YELLOW), "RUST_PRIMITIVE_TYPE": attr(PURPLE), "RUST_MODULE": attr(CYAN),
        "RUST_STRING": attr(GREEN), "RUST_NUMBER": attr(ORANGE), "RUST_COMMENT": attr(COMMENT, ft=I), "RUST_DOC_COMMENT": attr(COMMENT, ft=I),
        "RUST_VARIABLE": attr(CYAN), "RUST_PARAMETER": attr(CYAN), "RUST_MUT_BINDING": attr(CYAN, effect=DIM, effect_type=UNDERLINE),
        "RUST_OPERATORS": attr(RED),
        # TextMate bundles fallback (VS Code grammars inside IntelliJ)
        "TEXTMATE_COMMENT": attr(COMMENT, ft=I), "TEXTMATE_KEYWORD": attr(PURPLE, ft=I), "TEXTMATE_STRING": attr(GREEN),
        "TEXTMATE_NUMBER": attr(ORANGE), "TEXTMATE_CONSTANT": attr(RED), "TEXTMATE_VARIABLE": attr(CYAN), "TEXTMATE_FUNCTION": attr(YELLOW),
        "TEXTMATE_TYPE": attr(YELLOW), "TEXTMATE_TAG": attr(HOTPINK), "TEXTMATE_ATTRIBUTE": attr(YELLOW, ft=I), "TEXTMATE_MARKUP_HEADING": attr(PINK, ft=1),
        "TEXTMATE_MARKUP_BOLD": attr(ORANGE, ft=1), "TEXTMATE_MARKUP_ITALIC": attr(PURPLE, ft=2), "TEXTMATE_MARKUP_LIST": attr(YELLOW),
        "TEXTMATE_MARKUP_QUOTE": attr(COMMENT, ft=I), "TEXTMATE_MARKUP_RAW": attr(GREEN), "TEXTMATE_MARKUP_INSERTED": attr(GREEN),
        "TEXTMATE_MARKUP_DELETED": attr(RED), "TEXTMATE_MARKUP_CHANGED": attr(BLUE), "TEXTMATE_STORAGE": attr(PURPLE, ft=I),
        "TEXTMATE_ENTITY": attr(YELLOW), "TEXTMATE_SUPPORT": attr(YELLOW), "TEXTMATE_INVALID": attr(ERROR, ft=I),
    }

    lines = [f'<scheme name="{escape(name)}" version="142" parent_scheme="Darcula">',
             '  <metaInfo>',
             '    <property name="ide">idea</property>',
             '    <property name="ideVersion">2025.2.0.0</property>',
             '    <property name="originalScheme">' + escape(name) + '</property>',
             '  </metaInfo>',
             '  <option name="LINE_SPACING" value="1.2" />',
             '  <colors>']
    for k in sorted(colors):
        lines.append(f'    <option name="{k}" value="{colors[k]}" />')
    lines.append('  </colors>')
    lines.append('  <attributes>')
    for k in sorted(attrs):
        v = attrs[k]
        if not v:
            lines.append(f'    <option name="{k}" baseAttributes="TEXT" />')
            continue
        lines.append(f'    <option name="{k}">')
        lines.append('      <value>')
        for vk, vv in v.items():
            lines.append(f'        <option name="{vk}" value="{vv}" />')
        lines.append('      </value>')
        lines.append('    </option>')
    lines.append('  </attributes>')
    lines.append('</scheme>')
    OUT.mkdir(parents=True, exist_ok=True)
    stem = name.replace(" ", "")
    (OUT / f"{stem}.xml").write_text("\n".join(lines) + "\n")
    print("wrote", OUT / f"{stem}.xml", f"({len(attrs)} attributes, {len(colors)} colours)")


if __name__ == "__main__":
    build("Andromeda", bordered=False, italic=False)
    build("Andromeda Italic", bordered=False, italic=True)
    build("Andromeda Bordered", bordered=True, italic=False)
    build("Andromeda Italic Bordered", bordered=True, italic=True)
