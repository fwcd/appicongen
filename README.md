# Appicongen

A small CLI tool for generating app icon sets for macOS/iOS projects.

## Examples

```sh
# Generate AppIcon.appiconset from icon.png with iOS, macOS and watchOS icons
appicongen --all icon.png
```

```sh
# Generate MyIcon.appiconset from icon.png with only iOS icons
appicongen --ios -o MyIcon.appiconset icon.png
```

```sh
# Generate MyIcon.appiconset from icon.png with only macOS icons
# and automatically resize/mask the images to a rounded rectangle
# shape in the style of macOS Big Sur.
appicongen --macos --bigsurify -o MyIcon.appiconset icon.png
```
