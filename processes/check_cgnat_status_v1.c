#	- check_cgnat_status_v1.0.c
#	- Version 1.0
#	- Release day: Aug 02, 2016
#	- By Dat Nguyen Thanh - datnt11@fpt.com.vn
#---------------------Change log: ver 1.0-------------------------------------
# - check_show_chassis_routing_engine:	Status of routing_engine (current state, DRAM, status)
# - check_show_chassis_hardware:		Check if FPC are inserted or removed from chassis
# - check_show_chassis_fpc:				State, CPU, memory of FPC
# - check_show_chassis_fpc_pic_status: 	Check if MIC are inserted or removed from chassis and status
# - check_show_interfaces_terse:		Check status of physical interfaces
# - check_show_isis_adjacency:			Check ISIS interface, neighbor, level of interface, new and missing isis interface
# - check_show_isis_adjacency			Check ISIS interface, neighbor, level of interface, new and missing isis interface
# - check_show_mpls_interface:			Check mpls interface, neighbor, level of interface, new and missing mpls interface
# - check_show_rsvp_interface			Check rsvp interface, level of interface, new and missing rsvp interface
# - check_show_rsvp_neighbor			Check status of rsvp neighbor
# - check_show_ldp_neighbor:			Check ldp interface, neighbor, level of interface, new and missing ldp interface
# - check_show_bgp_summary:				Check number of BGP peers, status of neighbor (neighbor address, ASN, state)
# - check_show_route_instance_master	Check route of table inet.0, inet.3, iso.0, mpls.0, bgp.l3vpn.0, inet6.0, bgp.l2vpn.0, bgp.l3vpn-inet6.0
# - check_show_services_service-sets_cpu-usage_service-set_NAT;
# - check_show_services_service-sets_cpu-usage_service-set_NAT2;
# - check_show_services_flows_count_service-set_NAT;
# - check_show_services_flows_count_service-set_NAT2;
# - check_show_interfaces_load-balancing_detail;
# - check_show_services_service-sets_statistics_packet-drops;
# - check_show_services_service-sets_memory-usage_zone;
#-----------------------------------------------------------------------------


do {
	check_show_chassis_routing_engine;
	check_show_chassis_hardware; 	
	check_show_chassis_fpc; 
	check_show_chassis_fpc_pic_status;
	check_show_interfaces_terse;
	check_show_isis_interface;
	check_show_isis_adjacency;
	check_show_mpls_interface;
	check_show_rsvp_neighbor;
	check_show_rsvp_interface;	
	check_show_ldp_neighbor;
	check_show_bgp_summary;
	check_show_route_instance_master;
	check_show_services_service-sets_cpu-usage_service-set_NAT;
	check_show_services_service-sets_cpu-usage_service-set_NAT2;
	check_show_services_flows_count_service-set_NAT;
	check_show_services_flows_count_service-set_NAT2;
	check_show_interfaces_load-balancing_detail;
	check_show_services_service-sets_statistics_packet-drops;
	check_show_services_service-sets_statistics_syslog;
}
check_show_chassis_routing_engine {
	command show chassis routing-engine;
	iterate route-engine {
		id slot;
		no-diff status {
			info "Checking the routing-engine status...";
			err "ERROR:	Routing-Engine re%s has changed from %s to %s.", $ID.1, $PRE/status, $POST/status;
		}
		no-diff memory-dram-size {
			info "Checking the DRAM...";
			err "ERROR: DRAM of Routing Engine re%s has changed from %s to %s.", $ID.1, $PRE/memory-dram-size, $POST/memory-dram-size;
		}
		no-diff mastership-state {
			info "Checking Current state (master/backup)...";
			err "ERROR:	Routing Engine re%s has changed from %s to %s.", $ID.1, $PRE/mastership-state, $POST/mastership-state;
		}
	}
}
check_show_chassis_hardware {
	command show chassis hardware;
	iterate chassis/chassis-module {
		id name;
		list-not-less name {
			info "Checking for missing modules ...";
			err "ERROR: the module %s is missing.", $ID.1;
		}
		list-not-more name {
			info "Checking for new modules ...";
			err "ERROR: the module %s was installed.", $ID.1;
		}
		no-diff-in model-number {
			info "Checking chassis module model-number ...";
			err "ERROR: the model-number of module %s has changed from %s to %s.", $ID.1, $PRE/model-number, $POST/model-number;
		}
		no-diff-in serial-number {
			info "Checking chassis module serial-number ...";
			err "ERROR: the serial-number of module %s has changed from %s to %s.", $ID.1, $PRE/serial-number, $POST/serial-number;
		}

	}
	iterate chassis/chassis-module/chassis-sub-module {
		id name;
		id ../name;
		list-not-less name {
			info "Checking for missing sub-modules ...";
			err "ERROR: the sub-module %s of module %s is missing.", $ID.1, $ID.2;
		}
		list-not-more name {
			info "Checking for new sub-modules ...";
			err "ERROR: the sub-module %s of module %s was installed.", $ID.1, $ID.2;
		}
		no-diff name {
			info "Checking chassis sub-modules names ...";
			err "ERROR: the sub-module %s of module %s has changed from %s to %s.", $ID.1, $ID.2, $PRE/name, $POST/name;
		}
		no-diff-in model-number {
			info "Checking chassis sub-module model-number ...";
			err "ERROR: the model-number of sub-module %s of module %s has changed from %s to %s.", $ID.1, $ID.2, $PRE/model-number, $POST/model-number;
		}
		no-diff-in serial-number {
			info "Checking chassis sub-module serial-number ...";
			err "ERROR: the serial-number of sub-module %s of module %s has changed from %s to %s.", $ID.1, $ID.2, $PRE/serial-number, $POST/serial-number;
		}
	}
}
check_show_chassis_fpc {
	command show chassis fpc;
	iterate fpc {
		id slot;
		no-diff state {
			info "Checking FPC status ...";
			err "ERROR: The FPC slot %s has changed its state from %s to %s.", $ID.1, $PRE/state, $POST/state;
		}
		is-lt-in cpu-total, 20 {
			info "Checking if the CPU of FPC is less than 20 ...";
			err " ERROR: the CPU utilisation of FPC %s is greater than 20 (Before = %s / After = %s).", $ID.1, $PRE/cpu-total, $POST/cpu-total;
		}
		is-lt-in memory-heap-utilization, 70 {
			info "Checking if the memory heap utilisation of the FPCs is less than 50.";
			err "ERROR: The memory heap utilisation of FPC %s is greater than 50 (Before = %s / After = %s).", $ID.1, $PRE/memory-heap-utilization, $POST/memory-heap-utilization;
		}
		no-diff-in memory-dram-size {
			info "Checking FPC DRAM ...";
			err "ERROR: The DRAM of FPC slot %s has changed from %s to %s.", $ID.1, $PRE/memory-dram-size, $POST/memory-dram-size;
		}
		is-lt-in memory-buffer-utilization, 50 {
			info "Checking if the memory buffer utilisation of the FPCs is less than 50.";
			err "ERROR: The memory buffer utilisation of FPC %s is greater than 50 ( Before = %s / After = %s ).", $ID.1, $PRE/memory-buffer-utilization, $POST/memory-buffer-utilization;
		}
		
	}
}
check_show_chassis_fpc_pic_status {
	command show chassis fpc pic-status;
	iterate fpc/pic {
		id pic-slot;
		id ../slot;
		no-diff pic-type {
			info "Checking the PIC types ...";
			err "ERROR: the PIC type of PIC %s of FPC slot %s has changed from %s to %s.", $ID.1, $ID.2, $PRE/pic-type, $POST/pic-type;
		}
		no-diff pic-state {
			info "Checking the PIC state ...";
			err "ERROR: the state of PIC %s of FPC slot %s has changed from %s to %s.", $ID.1, $ID.2, $PRE/pic-state, $POST/pic-state;
		}
		list-not-less pic-slot {
			info "Checking for missing PICs ...";
			err "ERROR: the PIC %s of FPC slot %s is missing.", $ID.1, $ID.2;
		}
		list-not-more pic-slot {
			info "Checking for new PICs ...";
			err "ERROR: the PIC %s of FPC slot %s was installed.", $ID.1, $ID.2;
		}
	}
}
check_show_interfaces_terse {
	command show interfaces terse;
	iterate physical-interface {
		id name;
		no-diff oper-status {
			info "Checking PHY operational status of interfaces ...";
			err "ERROR: the operational status for interface %s has changed from %s to %s.", $ID.1, $PRE/oper-status, $POST/oper-status;
		}
		no-diff admin-status {
			info "Checking PHY admin status of interfaces ...";
			err "ERROR: the admin status for interface %s has changed from %s to %s.", $ID.1, $PRE/admin-status, $POST/admin-status;
		}	
		list-not-less name {
			info "Checking for missing interfaces at PHY level ...";
			err "ERROR: the interface %s is missing.", $ID.1;
		}
		list-not-more {
			info "Checking for new interfaces at PHY level ...";
			err "ERROR: the interface %s is new.", $ID.1;
		}
	}
}
check_show_isis_interface {
	command show isis interface;
	iterate isis-interface {
		id ./interface-name;
		no-diff interface-name {
			info "Checking the ISIS interface names ...";
			err "ERROR: the interface %s has changed its name from %s to %s.", $ID.1,$PRE/interface-name, $POST/interface-name;
		}
		no-diff circuit-type {
			info "Checking the ISIS circuit type ...";
			err "ERROR: the interface %s has changed its circuit type from %s to %s.", $ID.1, $PRE/circuit-type, $POST/circuit-type;
		}
		no-diff-in isis-interface-state-one {
			info "Checking the Level 1 interface state ...";
			err "ERROR: the interface %s has changed its Level 1 interface state from %s to %s.", $ID.1, $PRE/isis-interface-state-one, $POST/isis-interface-state-one;
		}
		no-diff-in isis-interface-state-two {
			info "Checking the Level 2 interface state ...";
			err "ERROR: the interface %s has changed its Level 2 interface state from %s to %s.", $ID.1, $PRE/isis-interface-state-two, $POST/isis-interface-state-two;
		}
		no-diff metric-one {
			info "Checking the interface Level 1 metric ...";
			err "ERROR: the Level 1 metric for interface %s has changed from %s to %s.", $ID.1, $PRE/metric-one, $POST/metric-one;
		}
		no-diff metric-two {
			info "Checking the interface Level 2 metric ...";
			err "ERROR: the Level 2 metric for interface %s has changed from %s to %s.", $ID.1, $PRE/metric-two, $POST/metric-two;
		}
		list-not-less interface-name {
			info "Checking for missing ISIS interfaces ...";
			err "ERROR: the interface %s is missing.", $ID.1;
		}
		list-not-more interface-name {
			info "Checking for new ISIS interfaces ...";
			err "ERROR: the interface %s was not configured before.", $ID.1;
		}
	}
}
check_show_isis_adjacency {
	command show isis adjacency;
	iterate isis-adjacency {
		id ./interface-name;
		no-diff interface-name {
			info "Checking the ISIS interface names ...";
			err "ERROR: the interface %s has changed from %s to %s.", $ID.1, $PRE/interface-name, $POST/interface-name;
		}
		no-diff system-name {
			info "Checking the ISIS neighbour ...";
			err "ERROR: the ISIS neighbour on interface %s has changed from %s to %s.", $ID.1, $PRE/system-name, $POST/system-name;
		}
		no-diff level {
			info "Checking the Level of the ISIS adjacency ...";
			err "ERROR: the ISIS Level on interface %s has changed from % to %s.",$ID.1, $PRE/level, $POST/level;
		}
		list-not-less {
			info "Checking for missing ISIS adjacencies ...";
			err "ERROR: the ISIS adjacency for interface %s is missing.", $ID.1;
		}
		list-not-more {
			info "Checking for new ISIS adjacencies ...";
			err "ERROR: the ISIS adjacency for interface %s was not configured before.", $ID.1;
		}
	}
}
check_show_mpls_interface {
		command show mpls interface;
		iterate mpls-interface {
		id interface-name;
		no-diff interface-name {
			info "Checking if there are changes in the name of the MPLS interfaces";
			err "ERROR: the interface %s has changed its name from %s to %s.", $PRE/interface-name, $POST/interface-name;
		}
		no-diff mpls-interface-state {
			info "Checking the MPLS interface state ...";
			err "ERROR: the interface %s has changed its state from %s to %s.", $ID.1, $PRE/mpls-interface-state, $POST/mpls-interface-state;
		}
		list-not-less interface-name {
			info "Checking for missing MPLS interfaces ...";
			err "ERROR: the interface %s has gone missing.", $ID.1;
		}
		list-not-more interface-name {
			info "Checking for new MPLS interfaces ...";
			err "ERROR: the interface %s was not present before.", $ID.1;
		}
	}
}
check_show_rsvp_interface {
	command show rsvp interface;
	iterate . {
		no-diff active-count {
			info "Checking the number of active RSVP interfaces ...";
			err "ERROR: the number of active RSVP interfaces has changed from %s to %s.", $PRE/active-count $POST/active-count;
		}
	}
	iterate rsvp-interface {
		id interface-name;
		no-diff interface-name {
			info "Checking if the name of the RSVP interface has changed ...";
			err "ERROR: the name of the RSVP interface %s has changed from %s to %s.", $ID.1, $PRE/interface-name, $POST/interface-name;
		}
		no-diff rsvp-status {
			info "Checking the RSVP status for each interface ...";
			err "ERROR: the status of the RSVP interface %s has changed from %s to %s.", $ID.1, $PRE/rsvp-status, $POST/rsvp-status;
		}
		list-not-less interface-name {
			info "Checking for missing RSVP interfaces ...";
			err "ERROR: the RSVP interface %s has gone missing.", $ID.1;
		}
		list-not-more interface-name {
			info "Checking for new RSVP interfaces ...";
			err "ERROR: the RSVP interface %s was not present before.", $ID.1;
		}
	}
}
check_show_rsvp_neighbor {
     command show rsvp neighbor detail;
     iterate rsvp-neighbor {
	 id rsvp-neighbor-address;
          no-diff rsvp-neighbor-status {
               info "Check RSVP neighbor status";
               err "ERROR: RSVP neighbor %s has changed from %s to %s.", $ID.1, $PRE/rsvp-neighbor-status, $POST/rsvp-neighbor-status;
          }
     }
}
check_show_ldp_neighbor {
    command show ldp neighbor;
    iterate ldp-neighbor {
		id ldp-neighbor-address;
		list-not-less ldp-neighbor-address {
			info "Checking for missing LDP neighbor ...";
			err " ERROR: The interface %s is missing.", $ID.1;
		}
		list-not-more ldp-neighbor-address {
			info "Checking for new LDP neighbor ...";
			err " ERROR: The interface %s is new.", $ID.1;
		}
	}
}
check_show_bgp_summary {
	command show bgp summary;
	iterate bgp-peer {
		id peer-address;
		id peer-as;
		no-diff peer-address {
			info "Checking if the BGP peers addresses are still the same ...";
			err "ERROR: the BGP peer %s (ASN %s) has changed its address from %s to %s.", $ID.1, $ID.2, $PRE/peer-address, $POST/peer-address;
		}
		no-diff peer-as {
			info "Checking if the BGP peers ASNs are still the same ...";
			err "ERROR: the ASN for the BGP peer %s has changed from %s to %s.", $ID.1. $PRE/peer-asn, $POST/peer-asn;
		}
		no-diff peer-state  {                                                                                         
			info "Checking status of BGP peers";                                            
			err "ERROR: the BGP peer %s (ASN %s) has changed from %s to %s.", $ID.1, $ID.2, $PRE/peer-state, $POST/peer-state;                      
		}                                                                                                             
	}
	                                                                                                                                                                                                                                                 #
}                                                                                                                                                                                                                                                     
check_show_route_instance_master {
     command show route instance master;
     iterate instance-core/instance-rib {
		id irib-name;
		delta irib-active-count, 20% {
			info "Check active route";
			err "ERROR: Number of active routes in table %s has changed more than 20 percent (before = %s / after = %s) ", $ID.1, $PRE/irib-active-count, $POST/irib-active-count;
		}
		delta irib-holddown-count, 20% {
			info "Check holddown route";
			err "ERROR: Number of holddown routes in table %s has changed more than 20 percent (before = %s / after = %s) ", $ID.1, $PRE/irib-holddown-count, $POST/irib-holddown-count;
		}
		delta irib-hidden-count, 20% {
			info "Check hidden route";
			err "ERROR: Number of hidden routes in table %s has changed more than 20 percent (before = %s / after = %s) ", $ID.1, $PRE/irib-hidden-count, $POST/irib-hidden-count;
		}
     }
}
check_show_services_service-sets_cpu-usage_service-set_NAT {
	command show services service-sets cpu-usage service-set NAT;
	iterate service-set-cpu-statistics {
		id interface-name;
		not-range cpu-utilization-percent, 20, 80 {
			info "Checking if cpu-usage of service-sets NAT out of range 20-80%";
			err "ERROR: Check cpu-usage of service-set NAT interface %s (before %s, after %s).", $ID.1, $PRE/cpu-utilization-percent, $POST/cpu-utilization-percent;
		}
	}
}
check_show_services_service-sets_cpu-usage_service-set_NAT2 {
	command show services service-sets cpu-usage service-set NAT2;
	iterate service-set-cpu-statistics {
		id interface-name;
		not-range cpu-utilization-percent, 20, 80 {
			info "Checking if cpu-usage of service-sets NAT2 out of range 20-80%";
			err "ERROR: Check cpu-usage of service-set NAT2 interface %s (before %s, after %s).", $ID.1, $PRE/cpu-utilization-percent, $POST/cpu-utilization-percent;
		}
	}
}
check_show_services_flows_count_service-set_NAT {
	command show services flows count service-set NAT;
	iterate service-sfw-flow-count {
		id interface-name;
		delta flow-count, 10% {
			info "Checking if services flow of service-set NAT has changed more than 10%";
			err "ERROR: Services flow of service-set NAT interface %s has changed more than 10 percent (before %s, after %s).", $ID.1, $PRE/flow-count, $POST/flow-count;
		}
	}
}
check_show_services_flows_count_service-set_NAT2 {
	command show services flows count service-set NAT2;
	iterate service-sfw-flow-count {
		id interface-name;
		delta flow-count, 10% {
			info "Checking if services flow of service-set NAT2 has changed more than 10%";
			err "ERROR: Services flow of service-set NAT2 interface %s has changed more than 10 percent (before %s, after %s).", $ID.1, $PRE/flow-count, $POST/flow-count;
		}
	}
}
check_show_interfaces_load-balancing_detail {
	command show interfaces load-balancing detail;
	iterate interface-load-balancing-member-detail/member-interface {
		id member-name;
		is-equal member-state, "Active" {
			info "Checking if load-balancing interface not Active";
			err "ERROR: Load-balancing interface %s is not Active (Current Status is %s).", $ID.1, $POST/member-state;
		}
	}
}
check_show_services_service-sets_statistics_packet-drops {
	command show services service-sets statistics packet-drops;
	iterate service-set-packet-drops {
		id interface-name;
		id service-set-name;
		no-diff cpulimit-drops {
			info "Checking if cpulimit-drops is not changed";
			err "ERROR: cpulimit-drops of interface %s service-set name %s has changed from %s to %s.", $ID.1, $ID.2, $PRE/cpulimit-drops, $POST/cpulimit-drops;
		}
		no-diff memlimit-drops {
			info "Checking if memorylimit-drops is not changed";
			err "ERROR: memorylimit-drops of interface %s service-set name %s has changed from %s to %s.", $ID.1, $ID.2, $PRE/memlimit-drops, $POST/memlimit-drops;
		}
		no-diff flowlimit-drops {
			info "Checking if flowlimit-drops is not changed";
			err "ERROR: flowlimit-drops of interface %s service-set name %s has changed from %s to %s.", $ID.1, $ID.2, $PRE/flowlimit-drops, $POST/flowlimit-drops;
		}
	}
}
check_show_services_service-sets_statistics_syslog {
#show services service-sets statistics syslog | display xml | match "interface-name|global-dropped" 
	command show services service-sets statistics syslog;
	iterate	syslog-stats-global-dropped {
		id ./preceding-sibling::syslog-stats-interface-name[1];
		no-diff . {
			info "Checking syslog interfae drop";
			err "ERROR:  Service-sets statistics syslog of interface %s has changed from %s - POST %s", $ID.1 , $PRE/. , $POST/.;
		}
	}
}

