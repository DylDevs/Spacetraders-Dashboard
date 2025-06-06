import { Stage, Layer, Circle, Text } from 'react-konva';
import { GetSystems } from '@/components/webserver';
import React, { useEffect, useRef, useState } from 'react';

const SYSTEM_COLORS: Record<string, string> = {
  'NEUTRON_STAR': '#C0C0FF',
  'RED_STAR': '#FF4C4C',
  'ORANGE_STAR': '#FFA500',
  'BLUE_STAR': '#4C9CFF',
  'YOUNG_STAR': '#FFFF66',
  'WHITE_DWARF': '#E0E0E0',
  'BLACK_HOLE': '#222222',
  'HYPERGIANT': '#FFD700',
  'NEBULA': '#AA66FF',
  'UNSTABLE': '#FF00AA',
};

class System {
  symbol: string;
  x: number;
  y: number;
  agent: string | null;
  color: string;

  constructor({ symbol, type, x, y, agent }: any) {
    this.symbol = symbol;
    this.x = x;
    this.y = y;
    this.agent = agent;
    this.color = this.agent ? '#FFFF00' : SYSTEM_COLORS[type] || '#FFFFFF';
  }
}
const SYSTEM_CIRCLE_RADIUS = 25;
const ZOOM_SCALE = 1.15;

function Renderer() {
  const [systems, setSystems] = useState<System[]>([]);
  const stageRef = useRef<any>(null);
  const [scale, setScale] = useState(0.01);
  const [position, setPosition] = useState({ x: window.innerWidth / 2, y: window.innerHeight / 2 });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await GetSystems();
        setSystems(result.map((system: any) => new System(system)));
        console.log(result);
      } catch (error) {
        console.error('Error fetching systems:', error);
      }
    };

    fetchData();
  }, []);

  const handleWheel = (e: any) => {
    e.evt.preventDefault();

    const stage = stageRef.current;
    const oldScale = stage.scaleX();

    const pointer = stage.getPointerPosition();
    const direction = e.evt.deltaY > 0 ? 1 : -1;
    const newScale = direction > 0 ? oldScale / ZOOM_SCALE : oldScale * ZOOM_SCALE;

    const mousePointTo = {
      x: (pointer.x - stage.x()) / oldScale,
      y: (pointer.y - stage.y()) / oldScale,
    };

    const newPos = {
      x: pointer.x - mousePointTo.x * newScale,
      y: pointer.y - mousePointTo.y * newScale,
    };

    // Apply scale and position directly
    stage.scale({ x: newScale, y: newScale });
    stage.position(newPos);
    stage.batchDraw(); // Redraw immediately
  };

  return (
    <Stage width={window.innerWidth} height={window.innerHeight} draggable
    scaleX={scale} scaleY={scale} x={position.x} y={position.y}
    onWheel={handleWheel} ref={stageRef}>
      <Layer>
        {systems.map((system, index) => (
          <React.Fragment key={index}>
            <Circle
              x={system.x - SYSTEM_CIRCLE_RADIUS - 15}
              y={system.y + SYSTEM_CIRCLE_RADIUS}
              radius={SYSTEM_CIRCLE_RADIUS}
              fill={system.color}
            />
            {system.agent && (
              <Text
                x={system.x}
                y={system.y}
                text={system.agent}
                fontSize={50}
                fill="white"
              />
            )}
          </React.Fragment>
        ))}
      </Layer>
    </Stage>
  );
}

export default Renderer;
