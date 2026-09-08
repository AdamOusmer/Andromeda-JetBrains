package com.eliverlara.andromeda;

import com.intellij.lang.annotation.AnnotationHolder;
import com.intellij.lang.annotation.Annotator;
import com.intellij.lang.annotation.HighlightSeverity;
import com.intellij.lang.javascript.psi.JSCallExpression;
import com.intellij.lang.javascript.psi.JSExpression;
import com.intellij.lang.javascript.psi.JSLiteralExpression;
import com.intellij.lang.javascript.psi.JSReferenceExpression;
import com.intellij.lang.javascript.psi.JSThisExpression;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.psi.PsiElement;
import org.jetbrains.annotations.NotNull;

/**
 * Reproduces the TextMate scopes Andromeda colours in VS Code that IntelliJ's JavaScript highlighter does not expose:
 * <ul>
 *   <li>{@code execa} in {@code execa.stdout(...)}, {@code err.stderr} → variable.other.object → Orange</li>
 *   <li>{@code homeDir(...)}, {@code new Listr(...)} → entity.name.function → Yellow</li>
 *   <li>{@code true false null undefined} → constant.language → Red</li>
 *   <li>{@code this} → variable.language.this → Pink</li>
 * </ul>
 */
public final class AndromedaJsAnnotator implements Annotator {
    @Override
    public void annotate(@NotNull PsiElement element, @NotNull AnnotationHolder holder) {
        if (!AndromedaKeys.isAndromedaSchemeActive()) return;

        if (element instanceof JSThisExpression) {
            paint(holder, element, AndromedaKeys.THIS);
            return;
        }
        if (element instanceof JSLiteralExpression lit) {
            if (lit.isBooleanLiteral() || lit.isNullLiteral()) paint(holder, element, AndromedaKeys.LANGUAGE_CONSTANT);
            return;
        }
        if (!(element instanceof JSReferenceExpression ref)) return;

        PsiElement nameToken = ref.getReferenceNameElement();
        if (nameToken == null) return;
        PsiElement parent = ref.getParent();

        // homeDir(...) / execa.stdout(...) / new Listr(...) → Yellow
        if (parent instanceof JSCallExpression call && call.getMethodExpression() == ref) {
            paint(holder, nameToken, AndromedaKeys.FUNCTION_CALL);
            return;
        }
        // execa in execa.stdout, err in err.stderr, stderr in err.stderr.replace → Orange
        if (parent instanceof JSReferenceExpression outer && outer.getQualifier() == ref) {
            paint(holder, nameToken, AndromedaKeys.OBJECT);
            return;
        }
        // bare `undefined` → Red
        JSExpression qualifier = ref.getQualifier();
        if (qualifier == null && "undefined".equals(ref.getReferencedName())) {
            paint(holder, nameToken, AndromedaKeys.LANGUAGE_CONSTANT);
        }
    }

    private static void paint(AnnotationHolder holder, PsiElement range, TextAttributesKey key) {
        holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                .range(range)
                .enforcedTextAttributes(AndromedaKeys.resolve(key))
                .create();
    }
}
