def show_hero(title, subtitle, badges):
badge_html = ""

```
for badge in badges:
    badge_html += f'<span class="badge">{badge}</span>'

hero_html = f"""
<div class="hero">
    <div class="hero-top">
        SFC • SCF–IKARUS
    </div>

    <div class="hero-title">
        {title}
    </div>

    <div class="hero-subtitle">
        {subtitle}
    </div>

    <div>
        {badge_html}
    </div>
</div>
"""

st.markdown(
    hero_html,
    unsafe_allow_html=True,
)
```
