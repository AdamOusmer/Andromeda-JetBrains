package com.eliverlara.andromeda;

import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.colors.EditorColorsManager;
import com.intellij.openapi.editor.colors.EditorColorsScheme;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.editor.markup.TextAttributes;

/**
 * Attribute keys that give IntelliJ the TextMate-scope granularity Andromeda relies on in VS Code.
 * Colours live in the bundled Andromeda*.xml schemes; the fallbacks keep other schemes sane.
 */
public final class AndromedaKeys {
    private AndromedaKeys() {}

    /** variable.other.object.js / variable.other.object.property.js → Orange */
    public static final TextAttributesKey OBJECT =
            TextAttributesKey.createTextAttributesKey("ANDROMEDA_OBJECT", DefaultLanguageHighlighterColors.INSTANCE_FIELD);
    /** entity.name.function / support.function → Yellow */
    public static final TextAttributesKey FUNCTION_CALL =
            TextAttributesKey.createTextAttributesKey("ANDROMEDA_FUNCTION_CALL", DefaultLanguageHighlighterColors.FUNCTION_CALL);
    /** constant.language (true / false / null / undefined) → Red */
    public static final TextAttributesKey LANGUAGE_CONSTANT =
            TextAttributesKey.createTextAttributesKey("ANDROMEDA_LANGUAGE_CONSTANT", DefaultLanguageHighlighterColors.CONSTANT);
    /** variable.language.this → Pink */
    public static final TextAttributesKey THIS =
            TextAttributesKey.createTextAttributesKey("ANDROMEDA_THIS", DefaultLanguageHighlighterColors.KEYWORD);

    /** Only act while an Andromeda scheme is active, so other schemes keep IntelliJ's own semantics. */
    public static boolean isAndromedaSchemeActive() {
        EditorColorsScheme scheme = EditorColorsManager.getInstance().getGlobalScheme();
        String name = scheme.getName();
        if (name.startsWith("_@user_")) name = name.substring("_@user_".length());
        return name.startsWith("Andromeda");
    }

    /** Resolved attributes for the current scheme; used with enforcedTextAttributes so we win over the built-in highlighter. */
    public static TextAttributes resolve(TextAttributesKey key) {
        return EditorColorsManager.getInstance().getGlobalScheme().getAttributes(key);
    }
}
