# Accessible Alt Text for Figures

Use this guide when adding, improving, or reviewing `fig-alt` text for figures
and data visualizations in Quarto `.qmd` files.

## Core Goal

Write alt text that helps a screen reader user understand the figure without
duplicating the caption. The best descriptions are concise, specific, and based
on the plot code plus surrounding prose.

## What to Look At

- Plotting code: chart type, axis variables, groups, facets, encodings, fits
- Figure caption: the stated takeaway or context
- Surrounding prose: the point the figure is meant to support
- Data generation code: transformations, filters, and expected distributions

## Recommended Structure

1. Chart type: start with the chart type, such as "Scatter chart" or
   "Faceted histogram"
2. Data description: name the axes or main variables and any important
   encodings such as color, size, or panels
3. Key insight: describe the main pattern or comparison when it is not already
   obvious from the caption

## Writing Rules

- Start with the chart type, not with "Image of" or "Chart showing"
- Use plain language
- Include specific values or ranges when they matter
- Mention how many panels or facets are present when relevant
- Describe color only when color encodes data
- Do not repeat the caption verbatim

## Length Guide

- Simple charts: 2 to 3 sentences
- Standard charts: 3 to 4 sentences
- Complex or faceted charts: 4 to 5 sentences

## Template Patterns

### Scatter Chart

```text
Scatter chart. [X variable] along the x-axis, [Y variable] along the y-axis.
[Shape of the relationship]. [Key takeaway or notable range].
```

### Histogram

```text
Histogram of [variable]. [Shape: right-skewed, bimodal, normal, or uniform].
[Notable features such as gaps, outliers, or clusters].
```

### Bar Chart

```text
Bar chart. [Categories] along the x-axis, [measure] along the y-axis.
[Highest/lowest values and main comparison].
```

### Faceted Chart

```text
Faceted [chart type] with [N] panels, one per [facet variable].
[What is constant across panels]. [What varies and why it matters].
```

### Tile or Heatmap

```text
Tile chart. [Row variable] along the y-axis, [column variable] along the x-axis.
Color encodes [value]. [Where values are highest or lowest].
```

## Checklist

- [ ] Starts with chart type
- [ ] Names the important variables or axes
- [ ] Includes facets or encodings when they matter
- [ ] States the main pattern or takeaway
- [ ] Complements the caption instead of repeating it
- [ ] Uses concise, plain language

## Example

```markdown
#| fig-alt: |
#|   Faceted histogram with two panels stacked vertically. The top panel shows
#|   the original data with a bimodal distribution. The bottom panel shows the
#|   same data after z-score normalization, keeping the bimodal shape. A green
#|   normal curve overlaid on the bottom panel does not match the data, which
#|   shows that normalization changes scale but not distribution shape.
```

