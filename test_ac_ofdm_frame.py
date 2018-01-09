	def test_ac_ofdm_frame (self):
		mode = 1
		carriers_number = pow(2,10+mode)
		
		data_source = self.open_file_and_load_to_list()
		ac_index = self.aux_get_AC_index(mode)
		expected_ac = self.aux_expected_ac()
		
		
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
        result_ac = numpy.take(result, ac_index) # get the elements wich index are the element on ac_index


        self.assertFloatTuplesAlmostEqual(expected_ac, result_ac)
