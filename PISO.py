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

@block
def testbench():
	clk = Signal(bool(0))
	reset = ResetSignal(1,active=0,isasync=True)
	
	#PISO Signals
	parallel_in = Signal(intbv(0b1011)[4:]) # 4-bit input
	serial_out = Signal(bool(0))
	load = Signal(bool(0))
	
	#Instantiate PISO signals
	piso_inst =  PISO(clk, reset,parallel_in,serial_out, load)
	
	#Clock generation
	@always(delay(10))
	def clkgen():
		clk.next = not clk
		
	# Stimulus
	@instance
	def stimulus():
		#Apply reset
		print("Applying reset...")
		reset.next = 0
		yield clk.negedge
		reset.next = 1
		print("Reset deactivated...")
		
		#Load parallel data into PISO
		load.next = 1
		yield clk.negedge
		load.next = 0
		
		#Shift data out of PISO 
		for _ in range(4):
			yield clk.posedge
			print(f"PISO Serial Out: {serial_out}")
			
		raise StopSimulation()
		
	return piso_inst, clkgen, stimulus
	
#Run the testbench
tb = testbench()
tb.config_sim(trace=True)
tb.run_sim()		
