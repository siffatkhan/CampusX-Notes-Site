// Sifat Notes — shared Tailwind config (typography/spacing/radius only;
// colors are CSS custom properties in assets/theme.css so light/dark can swap).
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      borderRadius: {
        DEFAULT: "0.5rem",
        sm: "0.25rem",
        md: "0.75rem",
        lg: "1rem",
        xl: "1.5rem",
        full: "9999px"
      },
      spacing: {
        xs: "0.5rem",
        sm: "1rem",
        md: "1.5rem",
        lg: "2.5rem",
        xl: "4rem",
        "container-max": "1200px",
        gutter: "24px"
      },
      fontFamily: {
        h1: ["Geist", "sans-serif"],
        h2: ["Geist", "sans-serif"],
        h3: ["Geist", "sans-serif"],
        "label-caps": ["Geist", "sans-serif"],
        "body-lg": ["Inter", "sans-serif"],
        "body-md": ["Inter", "sans-serif"],
        "code-block": ["JetBrains Mono", "monospace"]
      },
      fontSize: {
        h1: ["40px", { lineHeight: "1.2", letterSpacing: "-0.02em", fontWeight: "600" }],
        "h1-mobile": ["32px", { lineHeight: "1.2", fontWeight: "600" }],
        h2: ["30px", { lineHeight: "1.3", fontWeight: "600" }],
        h3: ["24px", { lineHeight: "1.4", fontWeight: "500" }],
        "body-lg": ["18px", { lineHeight: "1.625", fontWeight: "400" }],
        "body-md": ["16px", { lineHeight: "1.625", fontWeight: "400" }],
        "code-block": ["14px", { lineHeight: "1.5", fontWeight: "400" }],
        "label-caps": ["12px", { lineHeight: "1", letterSpacing: "0.05em", fontWeight: "700" }]
      }
    }
  }
};
