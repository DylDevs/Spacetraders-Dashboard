import React, { useEffect, useRef, useState } from "react";
import { Application, Container, Graphics, Text, TextStyle, Ticker } from 'pixi.js';
import { GetSystems, GetWaypoints } from "@/components/webserver";
import { Circle } from "lucide-react";

function CircleRadius(x : number, y : number) {
    return Math.sqrt(x * x + y * y);
}

const SYSTEM_COLORS : Record<string, string> = {
    'NEUTRON_STAR': '#C0C0FF',     // Pale bluish-white, dense and faint
    'RED_STAR': '#FF4C4C',         // Bright red, clear on dark
    'ORANGE_STAR': '#FFA500',      // Classic orange, like K-type stars
    'BLUE_STAR': '#4C9CFF',        // Vivid blue, representing hot blue stars
    'YOUNG_STAR': '#FFFF66',       // Yellow-tinted white, young and energetic
    'WHITE_DWARF': '#E0E0E0',      // Dim white-grey, fading compact star
    'BLACK_HOLE': '#222222',       // Almost black but visible on navy
    'HYPERGIANT': '#FFD700',       // Gold, massive and luminous
    'NEBULA': '#AA66FF',           // Vivid purple, gas cloud with glow
    'UNSTABLE': '#FF00AA',         // Hot pink/magenta, chaotic vibe
}

const WAYPOINT_COLORS : Record<string, string> = {
    'PLANET': '#3FA34D',                  // Earth-like green, natural and prominent
    'GAS_GIANT': '#1E90FF',               // Deep sky blue, massive and vibrant
    'MOON': '#AAAAAA',                    // Pale grey, muted but distinct
    'ORBITAL_STATION': '#CCCCFF',         // Soft blue-grey, industrial and visible
    'JUMP_GATE': '#FF69B4',               // Hot pink, sci-fi energy feel
    'ASTEROID_FIELD': '#8B7D7B',          // Dusty brown-grey, cluttered zone feel
    'ASTEROID': '#6E6E6E',                // Solid dark grey
    'ENGINEERED_ASTEROID': '#FFB347',     // Orange-tan, shows artificial tampering
    'ASTEROID_BASE': '#B5651D',           // Rich brown, grounded and hidden
    'NEBULA': '#8A2BE2',                  // Deep violet, gaseous glow
    'DEBRIS_FIELD': '#808080',            // Neutral grey, floating junk
    'GRAVITY_WELL': '#00CED1',            // Bright cyan, intense pull
    'ARTIFICIAL_GRAVITY_WELL': '#7FFFD4', // Aquamarine, techy gravity zone
    'FUEL_STATION': '#FFD700',            // Bright gold, quick recognition
    'ORBITAL': '#A0C4FF',                 // Soft light blue, general orbit marker
}
const FADE_STEP = 0.05

const fade = (obj: { alpha: number }, type: "in" | "out", onComplete: () => void = () => {}) => {
    const fadeTicker = new Ticker();
    let done = false
    fadeTicker.add(() => {
        if (type === "in") {
            obj.alpha += FADE_STEP;
            if (obj.alpha > 1) {
                obj.alpha = 1;
                done = true
            }
        } else if (type === "out") {
            obj.alpha -= FADE_STEP;
            if (obj.alpha < 0) {
                obj.alpha = 0;
                done = true
            }
        }

        if (done) {
            fadeTicker.stop();
            onComplete();
        }
    });
    fadeTicker.start();
};

export default function SpaceTradersDashboard() {
    const [display, setDisplay] = useState<"systems" | "waypoints">("waypoints");
    const pixiAppRef = useRef<Application | null>(null);
    const canvasContainerRef = useRef<HTMLDivElement>(null);
    const containerRef = useRef<Container | null>(null);
    const isDraggingRef = useRef(false);
    const lastPositionRef = useRef({ x: 0, y: 0 });
    const scaleRef = useRef(1);

    // Initialize and cleanup PixiJS
    useEffect(() => {
        const initPixi = async () => {
            if (!canvasContainerRef.current || pixiAppRef.current) return;

            // Create and initialize the PixiJS application
            const app = new Application();
            await app.init({
                background: 0x000712,
                resizeTo: window,
                antialias: true
            });

            pixiAppRef.current = app;
            canvasContainerRef.current.appendChild(app.canvas);

            // Create a container for all our interactive elements
            const container = new Container();
            containerRef.current = container;
            app.stage.addChild(container);

            // Center the container initially
            container.x = app.screen.width / 2;
            container.y = app.screen.height / 2;

            // Add event listeners for zoom and pan
            setupInteractivity(app, container);

            // Create display based on current state
            if (display === "systems") {
                await createSystemsDisplay(container);
            } else {
                await createWaypointsDisplay(container);
            }
        };

        initPixi();

        return () => {
            // Cleanup when component unmounts or display changes
            if (pixiAppRef.current) {
                pixiAppRef.current.destroy(true);
                pixiAppRef.current = null;
                containerRef.current = null;
            }
        };
    }, [display]);

    function setupInteractivity(app: Application, container: Container) {
        if (!app.view) return;

        // Pan functionality
        app.view.addEventListener('mousedown', (e) => {
            isDraggingRef.current = true;
            lastPositionRef.current = {
                x: e.clientX,
                y: e.clientY
            };
            app.view.style.cursor = 'grabbing';
        });

        app.view.addEventListener('mousemove', (e) => {
            if (!isDraggingRef.current) return;
            
            const dx = e.clientX - lastPositionRef.current.x;
            const dy = e.clientY - lastPositionRef.current.y;
            
            container.x += dx;
            container.y += dy;
            
            lastPositionRef.current = {
                x: e.clientX,
                y: e.clientY
            };
        });

        app.view.addEventListener('mouseup', () => {
            isDraggingRef.current = false;
            app.view.style.cursor = 'grab';
        });

        app.view.addEventListener('mouseleave', () => {
            isDraggingRef.current = false;
            app.view.style.cursor = 'default';
        });

        app.view.style.cursor = 'grab';

        // Zoom functionality
        app.view.addEventListener('wheel', (e) => {
            e.preventDefault();
            
            const zoomSpeed = 0.1;
            const delta = e.deltaY > 0 ? 1 - zoomSpeed : 1 + zoomSpeed;
            
            // Limit zoom levels
            const newScale = scaleRef.current * delta;
            if (newScale < 0.01 || newScale > 150) return;
            
            scaleRef.current = newScale;
            
            // Get mouse position relative to container
            const mouseX = e.clientX - container.x;
            const mouseY = e.clientY - container.y;
            
            // Apply zoom centered on mouse position
            container.scale.set(scaleRef.current);
            
            // Adjust position to zoom toward mouse
            container.x = e.clientX - mouseX * scaleRef.current;
            container.y = e.clientY - mouseY * scaleRef.current;
        });
    }

    async function createSystemsDisplay(container: Container) {
        if (!pixiAppRef.current) return;

        // Clear previous children
        container.removeChildren();

        const systems = await GetSystems();

        for (const system of systems) {
            const dot = new Graphics();
            dot.beginFill(SYSTEM_COLORS[system.type]);
            dot.drawCircle(0, 0, system.agent === null ? 50 : 100);
            dot.endFill();
            dot.x = system.x;
            dot.y = system.y;
            container.addChild(dot);
            
            if (system.agent === null) continue;
            const label = new Text(system.agent, {
                fontFamily: 'Arial',
                fontSize: 150,
                fill: 0xFFFF00,
            } as TextStyle);
            label.x = system.x + 150;
            label.y = system.y + 50;
            container.addChild(label);
        }
    }

    async function createWaypointsDisplay(container: Container) {
        if (!pixiAppRef.current) return;
        container.removeChildren();

        const loadingContainer = new Container();
        const contentContainer = new Container();

        const loading = new Text("Loading...", {
            fontFamily: 'Arial',
            fontSize: 20,
            fill: 0x444444,
        } as TextStyle);
        loading.anchor.set(0.5);
        loading.x = 0;
        loading.y = 0;
        
        const spinner = new Graphics();
        spinner.lineStyle(2, 0x444444);
        spinner.arc(0, 0, 15, 0, Math.PI * 1.5);
        spinner.x = 0;
        spinner.y = 30;

        loadingContainer.addChild(loading, spinner);
        container.addChild(loadingContainer);

        // Animate spinner
        const spinTicker = new Ticker();
        spinTicker.add(() => {
            spinner.rotation += 0.1;
        });
        spinTicker.start();

        const system_waypoints = await GetWaypoints();
        console.log(system_waypoints);

        for (const waypoint of system_waypoints.waypoints) {
            const dot = new Graphics();
            dot.beginFill(WAYPOINT_COLORS[waypoint.type]);
            dot.drawCircle(waypoint.x, waypoint.y, 7);
            dot.endFill();
            contentContainer.addChild(dot);

            const orbit_ring = new Graphics();
            orbit_ring.lineStyle(1, 0x444444, 0.5);
            orbit_ring.beginFill(0, 0);
            orbit_ring.drawCircle(0, 0, CircleRadius(waypoint.x, waypoint.y));
            orbit_ring.endFill();
            contentContainer.addChild(orbit_ring);
        }

        fade(loadingContainer, "out", () => {
            container.removeChild(loadingContainer);
            spinTicker.stop();
        });

        fade(contentContainer, "in");
    }

    return (
        <div ref={canvasContainerRef} />
    );
}