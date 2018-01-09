def test_tmcc_ofdm_frame (self):
		mode = 1
		carriers_number = pow(2,10+mode)
		
		data_source = self.open_file_and_load_to_list()
		
		
		# Example of param_layer_A:
		# str carrier_mod_scheme = "DQPSK"
		# str conv_coding_rate = "3/4"
		# int interleaving_length = 8
		# int number_of_segments = 12
		
		param_layer_A = ("DQPSK", "3/4", 8, 6)
		param_layer_B = ("QPSK", "1/2", 16, 6)
		param_layer_C = ("UNUSED", "UNUSED", "UNUSED", "UNUSED")
		
		expected_tmcc = self.aux_expected_tmcc(data_source, mode, param_layer_A, param_layer_B, param_layer_C)  # es un array de numpy
		tmcc_index = self.aux_get_TMCC_index(mode)
		
		
		##########
        # Bloques
        ##########
        src1 = blocks.vector_source_c(data_source, False, 96*13)
        dst = blocks.vector_sink_c(carriers_number)
        sqr = isdbt.ofdm_frame_structure(carriers_number)

        ############
        # Conexiones
        ############
        self.tb.connect(src1, sqr)
        self.tb.connect(sqr, dst)
        self.tb.run()

        result = dst.data()
        result_tmcc = numpy.take(result, tmcc_index) # get the elements wich index are the element on tmcc_index


        self.assertFloatTuplesAlmostEqual(expected_tmcc, result_tmcc)
			
