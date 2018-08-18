Network failure simulator tool written in python


=> Builds network graph object

=> Produces a topology layout diagram

=> Estimates traffix matrix based on the gravity model

=> what-if analysis - fails every P node and computes worst case link utilisations


HOW TO USE:

1. Provide the following files which tool will use as an input:


links.txt file contains the list of edges and weights
pe_traffic file contains traffic sources and sinks (pe devices) and traffic_in, traffic_out for each pe.


2. Run network_failure_simulator.py



3. Observe the wc_results.txt file