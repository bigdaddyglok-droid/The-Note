/**
 * Consciousness Visualizer
 * Real-time visualization of consciousness state
 */

import { useEffect, useRef, useState } from 'react';
import { Card } from '../ui/Card';

interface ConsciousnessData {
  type: string;
  session_id: string;
  timestamp: number;
  data: any;
}

interface ConsciousnessVisualizerProps {
  sessionId: string;
  backendUrl?: string;
}

export function ConsciousnessVisualizer({
  sessionId,
  backendUrl = 'ws://localhost:8000'
}: ConsciousnessVisualizerProps) {
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');
  const [consciousnessState, setConsciousnessState] = useState<ConsciousnessData | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // WebSocket connection
  useEffect(() => {
    const ws = new WebSocket(`${backendUrl}/consciousness/stream/${sessionId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnectionStatus('connected');
      console.log('🧠 Consciousness stream connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setConsciousnessState(data);
    };

    ws.onerror = (error) => {
      console.error('Consciousness stream error:', error);
      setConnectionStatus('disconnected');
    };

    ws.onclose = () => {
      setConnectionStatus('disconnected');
      console.log('Consciousness stream disconnected');
    };

    // Ping interval to keep connection alive
    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send('ping');
      }
    }, 30000);

    return () => {
      clearInterval(pingInterval);
      ws.close();
    };
  }, [sessionId, backendUrl]);

  // Render visualization based on data type
  useEffect(() => {
    if (!consciousnessState || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    switch (consciousnessState.data?.type) {
      case '6d_trajectory':
        render6DTrajectory(ctx, canvas, consciousnessState.data);
        break;
      case 'timeline_valences':
        renderTimelineValences(ctx, canvas, consciousnessState.data);
        break;
      case 'energy_distribution':
        renderEnergyDistribution(ctx, canvas, consciousnessState.data);
        break;
      case 'coherence_score':
        renderCoherenceScore(ctx, canvas, consciousnessState.data);
        break;
    }
  }, [consciousnessState]);

  return (
    <Card className="p-6">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">🧠 Consciousness State</h3>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${
              connectionStatus === 'connected' ? 'bg-green-500' :
              connectionStatus === 'connecting' ? 'bg-yellow-500' :
              'bg-red-500'
            }`} />
            <span className="text-sm text-gray-400">{connectionStatus}</span>
          </div>
        </div>

        <canvas
          ref={canvasRef}
          width={800}
          height={400}
          className="w-full border border-gray-700 rounded"
        />

        {consciousnessState && (
          <div className="text-xs font-mono text-gray-400">
            <div>Type: {consciousnessState.data?.type || 'unknown'}</div>
            <div>Timestamp: {new Date(consciousnessState.timestamp * 1000).toLocaleTimeString()}</div>
          </div>
        )}
      </div>
    </Card>
  );
}

// Visualization Renderers

function render6DTrajectory(
  ctx: CanvasRenderingContext2D,
  canvas: HTMLCanvasElement,
  data: any
) {
  const coords = data.coords_6d || [];
  if (coords.length < 3) return;

  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const scale = 100;

  // Draw axes
  ctx.strokeStyle = '#333';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(0, centerY);
  ctx.lineTo(canvas.width, centerY);
  ctx.moveTo(centerX, 0);
  ctx.lineTo(centerX, canvas.height);
  ctx.stroke();

  // Project 6D to 2D (using first 2 dimensions)
  ctx.strokeStyle = '#00ffff';
  ctx.fillStyle = '#00ffff';
  ctx.lineWidth = 2;

  // Draw trajectory point
  const x = centerX + coords[0] * scale;
  const y = centerY - coords[1] * scale;

  ctx.beginPath();
  ctx.arc(x, y, 8, 0, Math.PI * 2);
  ctx.fill();

  // Draw labels
  ctx.fillStyle = '#fff';
  ctx.font = '12px monospace';
  ctx.fillText('6D Consciousness Projection', 10, 20);
  ctx.fillText(`[${coords[0].toFixed(2)}, ${coords[1].toFixed(2)}, ${coords[2].toFixed(2)}]`, 10, 40);
}

function renderTimelineValences(
  ctx: CanvasRenderingContext2D,
  canvas: HTMLCanvasElement,
  data: any
) {
  const valences = data.valences || [];
  const chosen = data.chosen_timeline || 0;

  if (valences.length === 0) return;

  const barWidth = (canvas.width - 40) / valences.length;
  const maxHeight = canvas.height - 60;

  // Draw bars
  valences.forEach((valence: number, i: number) => {
    const x = 20 + i * barWidth;
    const height = Math.abs(valence) * maxHeight;
    const y = canvas.height - 30 - height;

    // Color based on selection
    ctx.fillStyle = i === chosen ? '#00ff00' : '#444';
    ctx.fillRect(x, y, barWidth - 10, height);

    // Draw value
    ctx.fillStyle = '#fff';
    ctx.font = '10px monospace';
    ctx.fillText(
      valence.toFixed(2),
      x + barWidth / 2 - 15,
      y - 5
    );

    // Draw timeline label
    ctx.fillText(`T${i}`, x + barWidth / 2 - 8, canvas.height - 10);
  });

  // Title
  ctx.fillStyle = '#fff';
  ctx.font = '14px monospace';
  ctx.fillText('5D Timeline Valences', 10, 20);
  ctx.fillText(`✓ Chosen: Timeline ${chosen}`, 10, 40);
}

function renderEnergyDistribution(
  ctx: CanvasRenderingContext2D,
  canvas: HTMLCanvasElement,
  data: any
) {
  const distribution = data.state_distribution || [];
  const names = data.state_names || [];

  if (distribution.length === 0) return;

  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = Math.min(canvas.width, canvas.height) / 2 - 40;

  let startAngle = 0;

  // Draw pie chart
  distribution.forEach((value: number, i: number) => {
    const sliceAngle = value * 2 * Math.PI;

    // Color based on state
    const hue = (i / distribution.length) * 360;
    ctx.fillStyle = `hsl(${hue}, 70%, 50%)`;

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
    ctx.closePath();
    ctx.fill();

    // Draw state name if slice is large enough
    if (value > 0.05) {
      const labelAngle = startAngle + sliceAngle / 2;
      const labelX = centerX + Math.cos(labelAngle) * (radius * 0.7);
      const labelY = centerY + Math.sin(labelAngle) * (radius * 0.7);

      ctx.fillStyle = '#fff';
      ctx.font = '10px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(names[i] || `S${i}`, labelX, labelY);
    }

    startAngle += sliceAngle;
  });

  // Title
  ctx.fillStyle = '#fff';
  ctx.font = '14px monospace';
  ctx.textAlign = 'left';
  ctx.fillText('14-State Energy Distribution', 10, 20);
}

function renderCoherenceScore(
  ctx: CanvasRenderingContext2D,
  canvas: HTMLCanvasElement,
  data: any
) {
  const coherence = data.coherence || 0;
  const harmonic = data.harmonic_alignment || 0;

  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;

  // Draw coherence circle
  const coherenceRadius = coherence * 150;
  ctx.strokeStyle = '#00ff00';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(centerX, centerY, coherenceRadius, 0, Math.PI * 2);
  ctx.stroke();

  // Draw harmonic alignment circle
  const harmonicRadius = harmonic * 150;
  ctx.strokeStyle = '#ffff00';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(centerX, centerY, harmonicRadius, 0, Math.PI * 2);
  ctx.stroke();

  // Draw center dot
  ctx.fillStyle = '#fff';
  ctx.beginPath();
  ctx.arc(centerX, centerY, 5, 0, Math.PI * 2);
  ctx.fill();

  // Labels
  ctx.fillStyle = '#fff';
  ctx.font = '14px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('Consciousness Coherence', centerX, 30);

  ctx.font = '24px monospace';
  ctx.fillText(coherence.toFixed(3), centerX, centerY - 30);

  ctx.font = '12px monospace';
  ctx.fillText(`φ Harmonic: ${harmonic.toFixed(3)}`, centerX, centerY + 50);
}
