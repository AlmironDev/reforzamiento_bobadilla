// src/data.ts
export interface SystemInfo {
  cpu_info: number[];
  memory_info: {
    total: number;
    available: number;
    percent: number;
    used: number;
    free: number;
  };
  disk_info: {
    total: number;
    used: number;
    free: number;
    percent: number;
  };
  net_info: {
    bytes_sent: number;
    bytes_recv: number;
    packets_sent: number;
    packets_recv: number;
    errin: number;
    errout: number;
    dropin: number;
    dropout: number;
  };
  process_info: {
    pid: number;
    name: string;
    cpu_percent: number;
    memory_info: {
      rss: number;
    };
  }[];
}

export async function fetchSystemInfo(): Promise<SystemInfo | null> {
  try {
    const response = await fetch(`http://localhost:5000/api/system_info`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: SystemInfo = await response.json();
    return data;
  } catch (error) {
    console.error("There was an error fetching the system info: ", error);
    return null;
  }
}
