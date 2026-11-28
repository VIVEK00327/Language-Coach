# Documentation Assets & Screenshot Registry

This folder stores application screenshots and diagrams for project documentation, thesis reports, and mentor presentations.

---

## Required Screenshots to Capture

Take these screenshots once running locally and save them with the exact filenames listed below:

| Target Filename | Page / Screen State | Visual Elements to Capture |
|---|---|---|
| `home-light.png` | `http://127.0.0.1:5000/` (Light Theme) | Hero section, animated sine wave, 4 language cards in light mode. |
| `home-dark.png` | `http://127.0.0.1:5000/` (Dark Theme) | Hero section, ambient glowing background, and language cards in dark mode. |
| `practice-recording.png` | `http://127.0.0.1:5000/practice` | Active recording state showing live waveform visualizer, volume meter, and circular timer ring. |
| `practice-results.png` | `http://127.0.0.1:5000/practice` | Assessment result view showing animated circular score ring, green/red sound chips, and coaching tip. |
| `progress-dashboard.png` | `http://127.0.0.1:5000/progress` | Summary statistics cards, HTML5 canvas score trend line chart, and recent attempts table. |
| `error-404.png` | `http://127.0.0.1:5000/non-existent` | Styled glassmorphic 404 Page Not Found with return home button. |

---

## Placeholders in Documentation

Documents use standard markdown image links with fallback TODO notes:
```markdown
![Home page in light theme](../assets/home-light.png)
*(TODO: Add screenshot of home-light.png)*
```
