type BubbleConfig = {
  id: string;
  size: number;
  left: string;
  duration: number;
  delay: number;
  driftX: number;
  opacity: number;
};

const bubbles: BubbleConfig[] = [
  {
    id: "bubble-01",
    size: 170,
    left: "6%",
    duration: 20,
    delay: 0,
    driftX: 18,
    opacity: 0.22,
  },
  {
    id: "bubble-02",
    size: 210,
    left: "16%",
    duration: 25,
    delay: 6,
    driftX: -12,
    opacity: 0.18,
  },
  {
    id: "bubble-03",
    size: 150,
    left: "29%",
    duration: 18,
    delay: 3,
    driftX: 14,
    opacity: 0.2,
  },
  {
    id: "bubble-04",
    size: 240,
    left: "41%",
    duration: 28,
    delay: 10,
    driftX: -16,
    opacity: 0.16,
  },
  {
    id: "bubble-05",
    size: 180,
    left: "54%",
    duration: 21,
    delay: 2,
    driftX: 10,
    opacity: 0.19,
  },
  {
    id: "bubble-06",
    size: 230,
    left: "67%",
    duration: 26,
    delay: 8,
    driftX: -20,
    opacity: 0.17,
  },
  {
    id: "bubble-07",
    size: 160,
    left: "79%",
    duration: 19,
    delay: 4,
    driftX: 16,
    opacity: 0.2,
  },
  {
    id: "bubble-08",
    size: 200,
    left: "89%",
    duration: 24,
    delay: 12,
    driftX: -10,
    opacity: 0.16,
  },
];

export default function AeroBubbleField() {
  return (
    <div className="aero-bubble-field" aria-hidden="true">
      {bubbles.map((bubble) => (
        <span
          key={bubble.id}
          className="aero-bubble-field__bubble"
          style={
            {
              "--bubble-size": `${bubble.size}px`,
              "--bubble-left": bubble.left,
              "--bubble-duration": `${bubble.duration}s`,
              "--bubble-delay": `${bubble.delay}s`,
              "--bubble-drift-x": `${bubble.driftX}px`,
              "--bubble-opacity": bubble.opacity,
            } as React.CSSProperties
          }
        />
      ))}
    </div>
  );
}