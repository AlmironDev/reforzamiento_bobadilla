interface InfoSystem {
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
    memory_info: any[]; // Especifícalo según los datos reales
    pid: number;
    cpu_percent: number;
    name: string;
  }[];
}
