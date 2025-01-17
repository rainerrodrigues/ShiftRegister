"""PISO Shift Register written in myHDL"""

from myhdl import block, always_seq, Signal,  intbv, ResetSignal, delay, instance, StopSimulation

@block
def PISOO(clk, reset, parallel_in, serial_out, load):
	"""
	Parallel-In Serial-Out (PISO) Shift Register
	
	clk		-- Clock Signal
	reset		-- Reset Signal
	parallel_in	-- Parallel data input
	serial_out	-- Serial data output
	load		-- Load control signal
	"""
	shift_reg = Signal(intbv(0)[len(parallel_in):]) #Internal shift register
	
	@always_seq(clk.posedge, reset=reset)
	def logic():
		if load: #load parallel data into the register
			shift_reg.next = parallel_in
		else:
			shift_reg.next = shift_reg >> 1
			
		# Output the least significant bit
		serial_out.next = shift_reg[0]
		
	return logic
		
