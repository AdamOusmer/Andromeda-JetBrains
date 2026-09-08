plugins {
    id("java")
    id("org.jetbrains.intellij.platform") version "2.11.0"
}

group = "com.eliverlara.andromeda"
version = "1.10.0"

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        // Set -PlocalIdePath=/path/to/IntelliJ IDEA.app to build against an installed IDE instead of downloading.
        val localIde = providers.gradleProperty("localIdePath").orNull
        if (localIde != null) local(localIde) else intellijIdeaCommunity("2025.2")
    }
}

intellijPlatform {
    buildSearchableOptions = false
    pluginConfiguration {
        name = "Andromeda Theme"
        ideaVersion {
            sinceBuild = "252"
            untilBuild = provider { null }
        }
    }
}


tasks.runIde {
    // Open the sample project when launched via ./gradlew runIde -PsampleProject=/path
    providers.gradleProperty("sampleProject").orNull?.let { args(it) }
    jvmArgs("-Didea.is.internal=true")
}
