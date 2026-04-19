# Responsive Design and Dark Mode

<cite>
**Referenced Files in This Document**
- [style.css](file://site/css/style.css)
- [base.html](file://templates/base.html)
- [index.html](file://templates/index.html)
- [blog.html](file://templates/blog.html)
- [post.html](file://templates/post.html)
- [links.html](file://templates/links.html)
- [build.py](file://build.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Conclusion](#conclusion)
10. [Appendices](#appendices)

## Introduction
This document explains Seisamuse’s responsive design and dark mode implementation. The site follows a mobile-first approach with a breakpoint at 640 pixels, ensuring optimal readability and usability across devices. Navigation adapts via a collapsible hamburger menu on small screens, while larger screens display a horizontal navigation bar. Dark mode is automatically enabled when the user’s system prefers dark appearance, switching color variables to reduce eye strain and improve battery life on OLED displays. Additional responsive features include a flexible grid layout for cards, sticky navigation with backdrop blur, and scalable typography.

## Project Structure
The site is a static site generated from Markdown content and Jinja2 templates. Styles are centralized in a single stylesheet, and the base template defines the navigation and layout structure used across pages.

```mermaid
graph TB
subgraph "Templates"
T_base["base.html"]
T_index["index.html"]
T_blog["blog.html"]
T_post["post.html"]
T_links["links.html"]
end
subgraph "Content"
C_posts["content/posts/*.md"]
C_about["content/about.md"]
end
subgraph "Site Output"
S_css["site/css/style.css"]
S_home["site/index.html"]
S_blog["site/blog/index.html"]
S_post["site/blog/{slug}.html"]
S_about["site/about/index.html"]
S_links["site/links/index.html"]
end
T_base --> S_home
T_index --> S_home
T_blog --> S_blog
T_post --> S_post
T_links --> S_links
T_base --> S_about
T_base --> S_links
C_posts --> S_post
C_about --> S_about
S_css --> S_home
S_css --> S_blog
S_css --> S_post
S_css --> S_about
S_css --> S_links
```

**Diagram sources**
- [base.html](file://templates/base.html)
- [index.html](file://templates/index.html)
- [blog.html](file://templates/blog.html)
- [post.html](file://templates/post.html)
- [links.html](file://templates/links.html)
- [style.css](file://site/css/style.css)
- [build.py](file://build.py)

**Section sources**
- [base.html](file://templates/base.html)
- [style.css](file://site/css/style.css)
- [build.py](file://build.py)

## Core Components
- Global color tokens and typography scale defined in the stylesheet root, enabling easy theme customization.
- Sticky navigation with backdrop blur and a mobile hamburger menu toggled via JavaScript in the base template.
- Responsive breakpoint at 640 pixels that adjusts font sizes, hero visuals, navigation layout, and card grid.
- Automatic dark mode using a media query that switches color tokens when the system prefers dark appearance.
- Flexible grid layout for link cards using CSS Grid with automatic column sizing.

**Section sources**
- [style.css](file://site/css/style.css)
- [base.html](file://templates/base.html)

## Architecture Overview
The responsive design and dark mode are implemented purely with CSS and minimal client-side JavaScript. The build process compiles templates and content into static HTML, embedding the stylesheet for runtime responsiveness.

```mermaid
sequenceDiagram
participant Browser as "Browser"
participant Template as "base.html"
participant CSS as "style.css"
participant Media as "@media (prefers-color-scheme : dark)"
participant NavJS as "nav-toggle onclick"
Browser->>Template : Load page
Template->>CSS : Apply styles
CSS->>Media : Evaluate system preference
Media-->>CSS : Switch color tokens if dark
Browser->>NavJS : Click hamburger icon
NavJS-->>Template : Toggle .nav-links.open class
Template-->>Browser : Render expanded mobile menu
```

**Diagram sources**
- [base.html](file://templates/base.html)
- [style.css](file://site/css/style.css)

## Detailed Component Analysis

### Responsive Breakpoint at 640px
- The breakpoint targets a common mobile threshold, optimizing spacing and readability for smaller screens.
- Adjustments include reducing the root font size, resizing hero avatar and headline, wrapping navigation items, hiding desktop navigation, and switching the link grid to a single column.

```mermaid
flowchart TD
Start(["Viewport Width"]) --> Check{"Width ≤ 640px?"}
Check --> |Yes| ApplyMobile["Apply mobile styles:<br/>- Reduced font size<br/>- Hero avatar/headline scaling<br/>- Wrap nav items<br/>- Hide desktop nav<br/>- Single-column grid"]
Check --> |No| Desktop["Desktop defaults:<br/>- Horizontal nav<br/>- Full-width grid"]
ApplyMobile --> End(["Rendered View"])
Desktop --> End
```

**Diagram sources**
- [style.css](file://site/css/style.css)

**Section sources**
- [style.css](file://site/css/style.css)

### Navigation System and Hamburger Menu
- The navigation is sticky and uses a translucent background with backdrop blur for depth and readability.
- On small screens, the desktop navigation list is hidden and replaced by a button that toggles visibility via a class on the navigation links container.
- The base template includes the toggle button and links, while the stylesheet controls layout and visibility.

```mermaid
sequenceDiagram
participant User as "User"
participant Button as "nav-toggle"
participant Nav as ".nav-links"
participant CSS as "style.css"
User->>Button : Click hamburger icon
Button->>Nav : Add/remove "open" class
CSS->>Nav : Display : flex or display : none
Nav-->>User : Expanded/collapsed menu
```

**Diagram sources**
- [base.html](file://templates/base.html)
- [style.css](file://site/css/style.css)

**Section sources**
- [base.html](file://templates/base.html)
- [style.css](file://site/css/style.css)

### Responsive Grid Layouts
- The link grid uses CSS Grid with an automatic column sizing policy that creates responsive cards without fixed breakpoints.
- At the 640px breakpoint, the grid switches to a single column to improve readability on small screens.

```mermaid
flowchart TD
GridStart["Grid Container"] --> Columns["Columns: auto-fill(minmax(280px, 1fr))"]
Columns --> SmallScreen{"Viewport ≤ 640px?"}
SmallScreen --> |Yes| Single["Single Column"]
SmallScreen --> |No| Multi["Multiple Columns"]
Single --> Render["Render Cards"]
Multi --> Render
```

**Diagram sources**
- [style.css](file://site/css/style.css)
- [links.html](file://templates/links.html)

**Section sources**
- [style.css](file://site/css/style.css)
- [links.html](file://templates/links.html)

### Dark Mode Implementation
- Dark mode is activated automatically when the user’s system prefers dark appearance using a media query.
- The media query overrides global color tokens to lighter text on darker backgrounds, adjusting accent colors and subtle borders for contrast and comfort.

```mermaid
flowchart TD
PrefersDark["System prefers dark?"] --> |Yes| Override["Override CSS variables:<br/>- Text, background<br/>- Accent, muted<br/>- Borders, card/code backgrounds"]
PrefersDark --> |No| Default["Use light theme tokens"]
Override --> Render["Render with dark tokens"]
Default --> Render
```

**Diagram sources**
- [style.css](file://site/css/style.css)

**Section sources**
- [style.css](file://site/css/style.css)

### Backdrop Filter and Sticky Positioning
- The navigation uses a semi-transparent background with a backdrop blur effect to visually integrate with page content while maintaining readability.
- Sticky positioning ensures the navigation remains at the top during scrolling, improving navigation continuity.

```mermaid
classDiagram
class Nav {
+background : var(--nav-bg)
+backdrop-filter : blur(8px)
+position : sticky
+top : 0
+z-index : 100
}
class NavLinks {
+display : flex
+gap : 1.5rem
}
class NavToggle {
+display : none
}
Nav --> NavLinks : "contains"
Nav --> NavToggle : "toggles"
```

**Diagram sources**
- [style.css](file://site/css/style.css)
- [base.html](file://templates/base.html)

**Section sources**
- [style.css](file://site/css/style.css)
- [base.html](file://templates/base.html)

### Responsive Typography Scaling
- Root font size scales down on small screens to improve legibility and reduce zooming on mobile devices.
- Headlines and body copy adjust proportionally to maintain visual hierarchy across breakpoints.

```mermaid
flowchart TD
FontBase["Root font-size"] --> Small{"Viewport ≤ 640px?"}
Small --> |Yes| Reduce["Reduce font-size slightly"]
Small --> |No| Normal["Keep default size"]
Reduce --> Headings["Scale headings and body"]
Normal --> Headings
Headings --> Render["Render with adjusted typography"]
```

**Diagram sources**
- [style.css](file://site/css/style.css)

**Section sources**
- [style.css](file://site/css/style.css)

### Page-Specific Layouts
- Home page includes a hero section with avatar, headline, subtitle, affiliation, bio, and social links, all responsive to screen size.
- Blog and post pages use lists and cards styled with consistent spacing and typography.
- Links page showcases a responsive grid of project cards.

```mermaid
graph LR
Home["index.html"] --> Hero["Hero section"]
Blog["blog.html"] --> PostList["Post list"]
Post["post.html"] --> PostHeader["Post header"]
Links["links.html"] --> CardGrid["Link grid"]
```

**Diagram sources**
- [index.html](file://templates/index.html)
- [blog.html](file://templates/blog.html)
- [post.html](file://templates/post.html)
- [links.html](file://templates/links.html)

**Section sources**
- [index.html](file://templates/index.html)
- [blog.html](file://templates/blog.html)
- [post.html](file://templates/post.html)
- [links.html](file://templates/links.html)

## Dependency Analysis
- The base template depends on the stylesheet for responsive behavior and dark mode.
- The build script compiles templates and content into static HTML, embedding the stylesheet and ensuring consistent rendering across pages.

```mermaid
graph TB
Build["build.py"] --> Templates["Jinja2 Templates"]
Build --> Content["Markdown Content"]
Templates --> HTML["Static HTML"]
Content --> HTML
HTML --> CSS["style.css"]
CSS --> Browser["Browser Rendering"]
```

**Diagram sources**
- [build.py](file://build.py)
- [style.css](file://site/css/style.css)

**Section sources**
- [build.py](file://build.py)
- [style.css](file://site/css/style.css)

## Performance Considerations
- CSS variables enable efficient theme switching without recalculating styles.
- Backdrop filter enhances visual depth with minimal performance cost on modern browsers.
- Sticky navigation reduces repeated layout thrashing by keeping the element in the visual viewport.
- Grid-based layouts minimize JavaScript dependencies and rely on native browser capabilities.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
- If the mobile menu does not appear:
  - Verify the hamburger button exists and toggles the “open” class on the navigation links container.
  - Confirm the stylesheet applies the mobile breakpoint and that the toggle button is visible below the breakpoint.
- If dark mode does not activate:
  - Ensure the media query for dark preferences is present and not overridden by higher specificity rules.
  - Test with the system preference set to dark and confirm the color tokens switch accordingly.
- If navigation overlaps content:
  - Check the sticky positioning and z-index values to ensure the navigation stays above other content.
- If grid layout appears broken:
  - Confirm the grid container uses the correct class and that the breakpoint rules apply at 640px.

**Section sources**
- [base.html](file://templates/base.html)
- [style.css](file://site/css/style.css)

## Conclusion
Seisamuse’s responsive design centers on a mobile-first approach with a 640px breakpoint, a flexible navigation system with a hamburger menu, and a robust grid layout. Dark mode is seamlessly integrated via a media query that switches color tokens based on user preference. Together, these features deliver a readable, accessible, and visually consistent experience across devices.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### Practical Testing Examples
- Resize the browser window to 640px or less to verify:
  - Reduced font size and scaled hero elements
  - Hidden desktop navigation and visible hamburger menu
  - Collapsed navigation menu when toggled
  - Single-column link grid
- Change the system appearance to dark and confirm:
  - Color tokens switch to dark variants
  - Navigation retains readability with backdrop blur
- Use the local preview server to test:
  - Run the build script with the serve option to preview changes locally.

**Section sources**
- [build.py](file://build.py)
- [style.css](file://site/css/style.css)
- [base.html](file://templates/base.html)

### Customizing Breakpoints
- To adjust the breakpoint:
  - Modify the media query condition in the stylesheet to a different pixel value.
  - Update related adjustments (font sizes, grid columns, navigation layout) consistently around the new breakpoint.
- To customize the mobile menu behavior:
  - Adjust the toggle button’s visibility and the navigation links’ display property in the stylesheet.
  - Ensure the base template’s toggle logic remains functional.

**Section sources**
- [style.css](file://site/css/style.css)
- [base.html](file://templates/base.html)