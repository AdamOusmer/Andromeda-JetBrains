package com.eliverlara.andromeda;

import com.intellij.lang.annotation.AnnotationHolder;
import com.intellij.lang.annotation.Annotator;
import com.intellij.lang.annotation.HighlightSeverity;
import com.intellij.psi.JavaTokenType;
import com.intellij.psi.PsiJavaToken;
import com.intellij.psi.PsiElement;
import com.intellij.psi.tree.IElementType;
import org.jetbrains.annotations.NotNull;

/** Java: {@code true false null} are constant.language in VS Code → Red, not keyword purple. */
public final class AndromedaJavaAnnotator implements Annotator {
    @Override
    public void annotate(@NotNull PsiElement element, @NotNull AnnotationHolder holder) {
        if (!(element instanceof PsiJavaToken token)) return;
        IElementType t = token.getTokenType();
        if (t != JavaTokenType.TRUE_KEYWORD && t != JavaTokenType.FALSE_KEYWORD && t != JavaTokenType.NULL_KEYWORD) return;
        if (!AndromedaKeys.isAndromedaSchemeActive()) return;
        holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                .range(element)
                .enforcedTextAttributes(AndromedaKeys.resolve(AndromedaKeys.LANGUAGE_CONSTANT))
                .create();
    }
}
