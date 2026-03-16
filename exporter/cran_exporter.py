"""
C-RAN Metrics Exporter for Prometheus

Collects and exposes metrics from Cloud-RAN infrastructure.

Author: Niloy Saha (niloyete@gmail.com)
Reference: IEEE INFOCOM 2024 - Experimental CRAN Platform
"""

import time
import random
import math
import logging
from prometheus_client import start_http_server, Gauge, Counter, Info

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('cran_exporter')

# System Info
system_info = Info('cran_system', 'C-RAN system information')

# Radio Unit Metrics
ru_signal_strength = Gauge(
    'cran_ru_signal_strength_dbm',
    'Signal strength at Radio Unit',
    ['ru_id', 'sector']
)
ru_active_ues = Gauge(
    'cran_ru_active_ues',
    'Active UEs connected to Radio Unit',
    ['ru_id', 'sector']
)
ru_prb_utilization = Gauge(
    'cran_ru_prb_utilization_percent',
    'PRB utilization percentage',
    ['ru_id', 'sector']
)

# Distributed Unit Metrics
du_throughput_dl = Gauge(
    'cran_du_throughput_dl_mbps',
    'Downlink throughput',
    ['du_id']
)
du_throughput_ul = Gauge(
    'cran_du_throughput_ul_mbps',
    'Uplink throughput',
    ['du_id']
)

# Central Unit Metrics
cu_cpu_usage = Gauge(
    'cran_cu_cpu_usage_percent',
    'CPU usage at Central Unit',
    ['cu_id']
)
cu_memory_usage = Gauge(
    'cran_cu_memory_usage_percent',
    'Memory usage at Central Unit',
    ['cu_id']
)

# Fronthaul Metrics
fronthaul_bandwidth = Gauge(
    'cran_fronthaul_bandwidth_gbps',
    'Fronthaul bandwidth usage',
    ['link_id']
)
fronthaul_latency = Gauge(
    'cran_fronthaul_latency_us',
    'Fronthaul latency',
    ['link_id']
)

# Event Counters
handover_total = Counter(
    'cran_handover_total',
    'Total handovers',
    ['ru_id', 'status']
)


class CRANSimulator:
    """Simulates C-RAN metrics with realistic patterns."""
    
    def __init__(self):
        self.time_step = 0
        self.rus = ['RU-001', 'RU-002', 'RU-003']
        self.sectors = ['alpha', 'beta', 'gamma']
        self.dus = ['DU-001', 'DU-002']
        self.cus = ['CU-001']
        self.fronthaul_links = ['FH-001', 'FH-002', 'FH-003']
        
        system_info.info({
            'version': '1.0.0',
            'ru_count': str(len(self.rus)),
            'du_count': str(len(self.dus))
        })
        logger.info("C-RAN Simulator initialized")
    
    def get_load_factor(self):
        """Daily traffic pattern simulation."""
        hour = (self.time_step % 1440) / 60
        morning = math.exp(-((hour - 10) ** 2) / 8)
        evening = math.exp(-((hour - 20) ** 2) / 8)
        return max(0.2, min(1.0, 0.3 + 0.5 * (morning + evening)))
    
    def collect_ru_metrics(self):
        load = self.get_load_factor()
        for ru_id in self.rus:
            for sector in self.sectors:
                ru_signal_strength.labels(ru_id=ru_id, sector=sector).set(
                    -75 + 15 * random.random()
                )
                ru_active_ues.labels(ru_id=ru_id, sector=sector).set(
                    int(30 * load) + random.randint(-5, 10)
                )
                ru_prb_utilization.labels(ru_id=ru_id, sector=sector).set(
                    min(95, 60 * load + 20 * random.random())
                )
                if random.random() < 0.05:
                    handover_total.labels(
                        ru_id=ru_id,
                        status='success' if random.random() > 0.1 else 'failed'
                    ).inc()
    
    def collect_du_metrics(self):
        load = self.get_load_factor()
        for du_id in self.dus:
            du_throughput_dl.labels(du_id=du_id).set(
                200 + 600 * load + 100 * random.random()
            )
            du_throughput_ul.labels(du_id=du_id).set(
                50 + 150 * load + 30 * random.random()
            )
    
    def collect_cu_metrics(self):
        load = self.get_load_factor()
        for cu_id in self.cus:
            cu_cpu_usage.labels(cu_id=cu_id).set(
                20 + 50 * load + 10 * random.random()
            )
            cu_memory_usage.labels(cu_id=cu_id).set(
                40 + 30 * load + 5 * random.random()
            )
    
    def collect_fronthaul_metrics(self):
        load = self.get_load_factor()
        for link_id in self.fronthaul_links:
            fronthaul_bandwidth.labels(link_id=link_id).set(
                5 + 15 * load + 2 * random.random()
            )
            fronthaul_latency.labels(link_id=link_id).set(
                20 + 30 * load + 10 * random.random()
            )
    
    def collect_all(self):
        self.time_step += 1
        self.collect_ru_metrics()
        self.collect_du_metrics()
        self.collect_cu_metrics()
        self.collect_fronthaul_metrics()
        
        if self.time_step % 60 == 0:
            logger.info(f"Step {self.time_step} | Load: {self.get_load_factor():.2f}")


def main():
    port = 8000
    interval = 10
    
    logger.info("=" * 50)
    logger.info("C-RAN Metrics Exporter Starting")
    logger.info(f"Port: {port} | Interval: {interval}s")
    logger.info("=" * 50)
    
    start_http_server(port)
    logger.info(f"Metrics: http://localhost:{port}/metrics")
    
    simulator = CRANSimulator()
    
    try:
        while True:
            simulator.collect_all()
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Shutting down...")


if __name__ == '__main__':
    main()
