# Tier Structure and Packaging

## How Many Tiers?

**2 tiers:** Simple, clear choice
- Works for: Clear SMB vs. Enterprise split
- Risk: May leave money on table

**3 tiers:** Industry standard
- Good tier = Entry point
- Better tier = Recommended (anchor to best)
- Best tier = High-value customers

**4+ tiers:** More granularity
- Works for: Wide range of customer sizes
- Risk: Decision paralysis, complexity

---

## Good-Better-Best Framework

**Good tier (Entry):**
- Purpose: Remove barriers to entry
- Includes: Core features, limited usage
- Price: Low, accessible
- Target: Small teams, try before you buy

**Better tier (Recommended):**
- Purpose: Where most customers land
- Includes: Full features, reasonable limits
- Price: Your "anchor" price
- Target: Growing teams, serious users

**Best tier (Premium):**
- Purpose: Capture high-value customers
- Includes: Everything, advanced features, higher limits
- Price: Premium (often 2-3x "Better")
- Target: Larger teams, power users, enterprises

---

## Tier Differentiation Strategies

**Feature gating:**
- Basic features in all tiers
- Advanced features in higher tiers
- Works when features have clear value differences

**Usage limits:**
- Same features, different limits
- More users, storage, API calls at higher tiers
- Works when value scales with usage

**Support level:**
- Email support → Priority support → Dedicated success
- Works for products with implementation complexity

**Access and customization:**
- API access, SSO, custom branding
- Works for enterprise differentiation

---

## Example Tier Structure

```
┌────────────────┬─────────────────┬─────────────────┬─────────────────┐
│                │ Starter         │ Pro             │ Business        │
│                │ $29/mo          │ $79/mo          │ $199/mo         │
├────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Users          │ Up to 5         │ Up to 20        │ Unlimited       │
│ Projects       │ 10              │ Unlimited       │ Unlimited       │
│ Storage        │ 5 GB            │ 50 GB           │ 500 GB          │
│ Integrations   │ 3               │ 10              │ Unlimited       │
│ Analytics      │ Basic           │ Advanced        │ Custom          │
│ Support        │ Email           │ Priority        │ Dedicated       │
│ API Access     │ ✗               │ ✓               │ ✓               │
│ SSO            │ ✗               │ ✗               │ ✓               │
│ Audit logs     │ ✗               │ ✗               │ ✓               │
└────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

---

## Packaging for Personas

### Identifying Pricing Personas

Different customers have different:
- Willingness to pay
- Feature needs
- Buying processes
- Value perception

**Segment by:**
- Company size (solopreneur → SMB → enterprise)
- Use case (marketing vs. sales vs. support)
- Sophistication (beginner → power user)
- Industry (different budget norms)

### Persona-Based Packaging

**Step 1: Define personas**

| Persona | Size | Needs | WTP | Example |
|---------|------|-------|-----|---------|
| Freelancer | 1 person | Basic features | Low | $19/mo |
| Small Team | 2-10 | Collaboration | Medium | $49/mo |
| Growing Co | 10-50 | Scale, integrations | Higher | $149/mo |
| Enterprise | 50+ | Security, support | High | Custom |

**Step 2: Map features to personas**
