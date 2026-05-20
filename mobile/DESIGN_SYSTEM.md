# Mobile Design System - Sentience Layer

## Overview
The mobile app now perfectly matches the frontend's premium **black-purple-gold** design system with consistent colors, typography, components, and interactions.

---

## Color Palette

### Backgrounds
- **Primary Background**: `#000000` (Pure black)
- **Secondary Background**: `#111111` (Dark gray)
- **Card Background**: `#111111`

### Primary Colors
- **Primary Neon**: `#7C3AED` (Purple)
- **Primary Glow**: `#A855F7` (Light purple)

### Accent Colors
- **Gold**: `#FCD34D` (Highlight text)
- **Text Body**: `#FDE68A` (Light yellow)
- **Text Muted**: `#D4D4D8` (Gray)

### Status Colors
- **Success**: `#22C55E` / `#10B981` (Green)
- **Danger**: `#EF4444` (Red)
- **Destructive**: `#EF4444`

### Borders
- **Border Light**: `rgba(124, 58, 237, 0.25)`
- **Border Medium**: `rgba(124, 58, 237, 0.5)`
- **Border Hover**: `rgba(124, 58, 237, 0.5)`

---

## Typography

### Variants
- **h1**: 28px, weight 800, letter-spacing 2
- **h2**: 20px, weight 800, letter-spacing 2
- **h3**: 16px, weight 700, letter-spacing 1.5
- **body**: 14px, weight 500, letter-spacing 0.5
- **bodyBold**: 14px, weight 700, letter-spacing 0.8
- **caption**: 11px, weight 700, letter-spacing 1
- **tiny**: 9px, weight 800, letter-spacing 1.5
- **button**: 12px, weight 800, letter-spacing 1.5

### Usage
```jsx
<Typography variant="h1" uppercase>Title</Typography>
<Typography variant="body">Body text</Typography>
<Typography variant="caption">Small text</Typography>
```

---

## Components

### Button
**Variants**: `primary`, `secondary`, `outline`, `ghost`, `destructive`
**Sizes**: `sm`, `default`, `lg`, `icon`

```jsx
<Button variant="primary" size="lg" onPress={handlePress}>
  <Typography variant="button" uppercase>CLICK ME</Typography>
</Button>
```

### Card
**Variants**: `default`, `elevated`, `glow`

```jsx
<Card variant="elevated" style={styles.card}>
  {children}
</Card>
```

### MetricsCard
Displays key metrics with trend indicators.

```jsx
<MetricsCard
  title="ACTIVE AGENTS"
  value={18}
  change={12}
  trend="up"
/>
```

### ChatBubble
Message bubbles with agent/user distinction, confidence badges, and action buttons.

```jsx
<ChatBubble
  isAgent={true}
  agentName="COGNITIVE KERNEL"
  message="Your message here"
  confidence={0.95}
/>
```

### TopBar
Consistent header across all screens.

```jsx
<TopBar
  title="SCREEN TITLE"
  subtitle="🧠 Subtitle text"
  showStatus={true}
/>
```

### BottomNav
Navigation bar with 4 main sections.

```jsx
<BottomNav
  activeRoute={activeRoute}
  onNavigate={setActiveRoute}
/>
```

### ActionCard
Cards for displaying actions/tasks with status badges.

```jsx
<ActionCard
  title="Task Name"
  description="Task description"
  status="active"
  onPress={handlePress}
/>
```

### SuggestedActions
Horizontal scrollable action chips.

```jsx
<SuggestedActions onAction={handleAction} />
```

### TypingIndicator
Animated typing indicator for chat.

```jsx
<TypingIndicator agentName="COGNITIVE KERNEL" />
```

---

## Shadows & Effects

### Neon Glow
```javascript
{
  shadowColor: '#A855F7',
  shadowOffset: { width: 0, height: 0 },
  shadowOpacity: 0.8,
  shadowRadius: 20,
  elevation: 15,
}
```

### Panel Shadow
```javascript
{
  shadowColor: '#000000',
  shadowOffset: { width: 0, height: 4 },
  shadowOpacity: 0.8,
  shadowRadius: 25,
  elevation: 10,
}
```

### Card Shadow
```javascript
{
  shadowColor: '#000000',
  shadowOffset: { width: 0, height: 4 },
  shadowOpacity: 0.5,
  shadowRadius: 15,
  elevation: 8,
}
```

### Button Glow
```javascript
{
  shadowColor: '#7C3AED',
  shadowOffset: { width: 0, height: 0 },
  shadowOpacity: 0.6,
  shadowRadius: 15,
  elevation: 8,
}
```

---

## Border Radius

- **sm**: 8px
- **md**: 12px
- **lg**: 16px
- **xl**: 20px
- **full**: 9999px (circular)

---

## Spacing Scale

- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **xxl**: 40px

---

## Screen Structure

### Standard Screen Layout
```jsx
<ScreenWrapper>
  <TopBar title="SCREEN TITLE" subtitle="Subtitle" />
  <ScrollView contentContainerStyle={styles.scroll}>
    {/* Content */}
  </ScrollView>
  <BottomNav activeRoute={route} onNavigate={setRoute} />
</ScreenWrapper>
```

---

## Updated Screens

1. **HomeScreen** - Hero section with modules grid
2. **ChatScreen** - Full chat interface with suggested actions
3. **DashboardScreen** - Metrics grid and activity feed
4. **CausalScreen** - Interactive causal graph explorer

---

## Design Principles

1. **Consistency**: All components use the same color palette and typography
2. **Hierarchy**: Clear visual hierarchy with h1 > h2 > h3 > body
3. **Contrast**: High contrast text on dark backgrounds for readability
4. **Glow Effects**: Purple neon glows for interactive elements
5. **Status Colors**: Green for success, red for errors, gold for highlights
6. **Uppercase**: Headers and buttons use uppercase for emphasis
7. **Letter Spacing**: Increased tracking for premium feel
8. **Shadows**: Deep shadows for depth and card elevation

---

## Frontend Alignment

The mobile design now matches the frontend exactly:
- ✅ Same color palette (black, purple, gold)
- ✅ Same typography scale and weights
- ✅ Same component variants (buttons, cards)
- ✅ Same status indicators and badges
- ✅ Same glow effects and shadows
- ✅ Same border styles and radius
- ✅ Same spacing and layout patterns

---

## Usage Example

```jsx
import { ScreenWrapper } from './components/ScreenWrapper';
import { TopBar } from './components/TopBar';
import { Card } from './components/Card';
import { Button } from './components/Button';
import { Typography } from './components/Typography';

export function MyScreen() {
  return (
    <ScreenWrapper>
      <TopBar title="MY SCREEN" subtitle="Description" />
      <ScrollView contentContainerStyle={{ padding: 20 }}>
        <Typography variant="h1" uppercase>Welcome</Typography>
        <Card variant="elevated">
          <Typography variant="body">Card content</Typography>
        </Card>
        <Button variant="primary" size="lg">
          <Typography variant="button" uppercase>ACTION</Typography>
        </Button>
      </ScrollView>
    </ScreenWrapper>
  );
}
```
