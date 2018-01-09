#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import isdbt_swig as isdbt
import cmath
import numpy
import operator

####################### GENERAL COMMENTS #######################
# - prefix aux_ denotes auxiliary functions for the tests
# - prefix test_ denotes functions where the test are processed
# - 



class qa_ofdm_frame (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None
    
    def aux_get_SP_index (self, mode):
        """Returns a vector with the SP indexes"""
        size = pow(2,10+mode)       #cantidad total de portadoras, incluyendo las SP,TMCC,AC.
        sp_step = 12                #una SP cada 12 portadoras
        sp_index_v = range(0,size,sp_step) #indices absolutos de las SP en un simbolo OFDM (0,12,24.48,...,2040 para modo 1)
        return sp_index_v

# Defines some auxiliary functions to make the tests

    def aux_get_TMCC_index (self, mode):
        """Returns a vector (various if mode > 1) with the TMCC indexs"""
        # los tmcc_index_mode son vectores cuyas entradas son el indice de TMCC absoluto en los 13 segmentos
        if mode == 1:
            tmcc_index_mode1 = (70+11*108, 25+9*108, 17+7*108, 86+5*108, 44+3*108, 47+1*108, 49, 31+2*108, 83+4*108, 61+6*108, 85+8*108, 101+10*108, 23+12*108)
            return tmcc_index_mode1

        if mode == 2:
            tmcc1_index_mode2 = (70+11*216, 17+9*216, 44+7*216, 49+5*216, 83+3*216, 85+1*216, 23, 25+2*216, 86+4*216, 47+6*216, 31+8*216, 61+10*216, 101+12*216)
            tmcc2_index_mode2 = (133+11*216, 194+9*216, 155+7*216, 139+5*216, 169+3*216, 209+1*216, 178, 125+2*216, 152+4*216, 157+6*216, 191+8*216, 193+10*216, 131+12*216)
            return tmcc1_index_mode2 + tmcc2_index_mode2

        if mode == 3:
            tmcc1_index_mode3 = (70+11*432, 44+9*432, 83+7*432, 23+5*432, 86+3*432, 31+1*432, 101, 17+2*432, 49+4*432, 85+6*432, 25+8*432, 47+10*432, 61+12*432)
            tmcc2_index_mode3 = (133+11*432, 155+9*432, 169+7*432, 178+5*432, 152+3*432, 191+1*432, 131, 194+2*432, 139+4*432, 209+6*432, 125+8*432, 157+10*432, 193+12*432)
            tmcc3_index_mode3 = (233+11*432, 265+9*432, 301+7*432, 241+5*432, 263+3*432, 277+1*432, 286, 260+2*432, 299+4*432, 239+6*432, 302+8*432, 247+10*432, 317+12*432)
            tmcc4_index_mode3 = (410+11*432, 355+9*432, 425+7*432, 341+5*432, 373+3*432, 409+1*432, 349, 371+2*432, 385+4*432, 394+6*432, 368+8*432, 407+10*432, 347+12*432)
            return tmcc1_index_mode3 + tmcc2_index_mode3 + tmcc3_index_mode3 + tmcc4_index_mode3
		# TODO: remover los 11*432 por algo no tan engorroso



    def aux_get_AC_index (self, mode):
        """Returns the AC index"""
        if mode == 1:
            ac1_index_mode1 = (10+11*108, 53+9*108, 61+7*108, 11+5*108, 20+3*108, 74+1*108, 35, 76+2*108, 4+4*108, 40+6*108, 8+8*108, 7+10*108, 98+12*108)
            ac2_index_mode1 = (28+11*108, 83+9*108, 100+7*108, 101+5*108, 40+3*108, 100+1*108, 79, 97+2*108, 89+4*108, 89+6*108, 64+8*108, 89+10*108, 101+12*108)
            return ac1_index_mode1 + ac2_index_mode1

        if mode == 2:
            ac1_index_mode2 = (10+11*216, 61+9*216, 20+7*216, 35+5*216, 4+3*216, 8+1*216, 98, 53+2*216, 11+4*216, 74+6*216, 76+8*216, 40+10*216, 7+12*216)
            ac2_index_mode2 = (28+11*216, 100+9*216, 40+7*216, 79+5*216, 89+3*216, 64+1*216, 101, 83+2*216, 101+4*216, 100+6*216, 97+8*216, 89+10*216, 89+12*216)
            ac3_index_mode2 = (161+11*216, 119+9*216, 182+7*216, 184+5*216, 148+3*216, 115+1*216, 118, 169+2*216, 128+4*216, 143+6*216, 112+8*216, 116+10*216, 206+12*216)
            ac4_index_mode2 = (191+11*216, 209+9*216, 208+7*216, 205+5*216, 197+3*216, 197+1*216, 136, 208+2*216, 148+4*216, 187+6*216, 197+8*216, 172+10*216, 209+12*216)
            return ac1_index_mode2 + ac2_index_mode2 + ac3_index_mode2 + ac4_index_mode2

        if mode == 3:
            ac1_index_mode3 = (10+11*432, 20+9*432, 4+7*432, 98+5*432, 11+3*432, 76+1*432, 7, 61+2*432, 35+4*432, 8+6*432, 53+8*432, 74+10*432, 40+12*432)
            ac2_index_mode3 = (28+11*432, 40+9*432, 89+7*432, 101+5*432, 101+3*432, 97+1*432, 89, 100+2*432, 79+4*432, 64+6*432, 83+8*432, 100+10*432, 89+12*432)
            ac3_index_mode3 = (161+11*432, 182+9*432, 148+7*432, 118+5*432, 128+3*432, 112+1*432, 206, 119+2*432, 184+4*432, 115+6*432, 169+8*432, 143+10*432, 116+12*432)
            ac4_index_mode3 = (191+11*432, 208+9*432, 197+7*432, 136+5*432, 148+3*432, 197+1*432, 209, 209+2*432, 205+4*432, 197+6*432, 208+8*432, 187+10*432, 172+12*432)
            ac5_index_mode3 = (277+11*432, 251+9*432, 224+7*432, 269+5*432, 290+3*432, 256+1*432, 226, 236+2*432, 220+4*432, 314+6*432, 227+8*432, 292+10*432, 223+12*432)
            ac6_index_mode3 = (316+11*432, 295+9*432, 280+7*432, 299+5*432, 316+3*432, 305+1*432, 244, 256+2*432, 305+4*432, 317+6*432, 317+8*432, 313+10*432, 305+12*432)
            ac7_index_mode3 = (335+11*432, 400+9*432, 331+7*432, 385+5*432, 359+3*432, 332+1*432, 377, 398+2*432, 364+4*432, 334+6*432, 344+8*432, 328+10*432, 422+12*432)
            ac8_index_mode3 = (425+11*432, 421+9*432, 413+7*432, 424+5*432, 403+3*432, 388+1*432, 407, 424+2*432, 413+4*432, 352+6*432, 364+8*432, 413+10*432, 425+12*432)
            return ac1_index_mode3 + ac2_index_mode3 + ac3_index_mode3 + ac4_index_mode3 + ac5_index_mode3 + ac6_index_mode3 + ac7_index_mode3 + ac8_index_mode3




    # def aux_expected_data (data_source, mode):

    #     j = 0
    #     for i in range(pow(2,10+mode)):
    #         # This loop generates the data in the expected result vector
    #         if i is not (sp_index + tmcc_index + ac_index):
    #             data_out[j] = data_source[i]
    #             j += 1
    #     return data_out




    def aux_get_data (self, ofdm_frame, mode):
        '''
        Extracts the data from the OFDM frame produced ignoring the TMCC, SP, AC
        
        :param tuple:       ofdm_frame expects the 13 OFDM frames
        :param int mode:    transmission mode
        ''' 
        sp_index = self.aux_get_SP_index(mode)
        tmcc_index = self.aux_get_TMCC_index(mode)
        ac_index = self.aux_get_AC_index(mode)
        data_result = []

        for i in range(pow(2,10+mode)):
            if i is not (sp_index + tmcc_index + ac_index):
                data_result.append(ofdm_frame[i])

        return data_result




    def aux_tplayer_info (self, mode, param_layer):
        """Takes the parameters for some layer and .,..
        :param param_layer: tuple with the parameters
        """
        expected_param_layer = numpy.array([0]*13)
        
        # Carrier modulation scheme
        carrier_mod_scheme = {"DQPSK": 0, "QPSK": 1, "16QAM": 2, "64QAM": 3, "RESERVED4":4, "RESERVED5": 5, "RESERVED6": 6, "UNUSED": 7}
        binary_repr = numpy.binary_repr(carrier_mod_scheme[param_layer[1]])
        expected_param_layer[[range(0,4)]] = numpy.array(list(binary_repr), dtype=int)

        # Convolutional Coding rate
        conv_coding_rate = {"1/2": 0, "2/3": 1, "3/4": 2, "5/6": 3, "RESERVED4":4, "RESERVED5": 5, "RESERVED6": 6, "UNUSED": 7}
        binary_repr = numpy.binary_repr(conv_coding_rate[param_layer[2]])
        expected_param_layer[[range(4,7)]] = numpy.array(list(binary_repr), dtype=int)

        # Interleaving length
        interleaving_length = {(0,1): 0, (0,2): 0, (0,3): 0, (4,1): 1, (2,2): 1, (1,3): 1, (8,1): 2, (4,2): 2, (2,3): 2, (16,1): 3, (8,2): 3, (4,3): 3, "RESERVED4":4, "RESERVED5": 5, "RESERVED6": 6, "UNUSED": 7}
        binary_repr = numpy.binary_repr(interleaving_length[(param_layer[3], mode)])
        expected_param_layer[[range(7,10)]] = numpy.array(list(binary_repr), dtype=int)

        # Number of segments
        number_of_segments = {"RESERVED0": 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, "RESERVED14": 14, "UNUSED": 15}
        binary_repr = numpy.binary_repr(number_of_segments[param_layer[4]])
        expected_param_layer[[range(10,14)]] = numpy.array(list(binary_repr), dtype=int)

        # expected_param_layer = (carrier_mod_scheme, conv_coding_rate, interleaving_length, nsegments)
        return expected_param_layer




    def aux_expected_tmcc (self, data_source, mode, param_layer_A, param_layer_B, param_layer_C):
        """Size 204"""
        tmcc = numpy.array([0]*204)

        # 1-16 Synchronizing signal. The alrternation test between w0 and w1, will be made in test_tmcc_ofdm_frame
        w0 = numpy.array([0,0,1,1,0,1,0,1,1,1,1,0,1,1,1,0])
        tmcc[[range(1,17)]] = w0

        # 17-19 Segment type identification: 000 for synchronous
        tmcc[[17,18,19]] = 0

        # 20-21 System identification: 00 for this standard ARIB STD – B31
        tmcc[[20,21]] = 0

        # 22-25 Indicator of transmission parameter switching: 1111 Normal value.
        tmcc[[range(22,26)]] = 1

        # 26 Emergency flag: 0 No startup control
        tmcc[[26]] = 0

        # CURRENT INFORMATION
        # 27 Partial reception flag: 1 Partial reception available
        tmcc[[27]] = 1

        # Transmission parameter information for LAYER A
        tmcc[[range(28,41)]] = aux_tplayer_info(mode, param_layer_A)

        # Transmission parameter information for LAYER B
        tmcc[[range(41,54)]] = aux_tplayer_info(mode, param_layer_B)

        # Transmission parameter information for LAYER C
        tmcc[[range(54,67)]] = aux_tplayer_info(mode, param_layer_C)

        # NEXT INFORMATION
        # Assume that the system parameters not changes
        tmcc[[range(67,107)]] = tmcc[[range(27,67)]]

        # 107- 109 Phase shift correction value for connected segment transmission (1 for all bits)
        tmcc[[range(107,110)]] = 1

        # 110-121 Reserved bits (1 for all)
        tmcc[[range(110, 122)]] = 1

        return tmcc



    def aux_expected_ac (self):
        """Sets the Auxiliary Channel expected (this is optional, so we fill with zeros)"""

        expected_ac = numpy.array([0]*204) 
        return expected_ac




    def aux_expected_sp (self, data_source, mode):
		"""TODO: implementar esto y ver lo de la PRBS"""
        self.tb = None





    def open_file_and_load_to_list (self, file_path):
        """Opens a file source and load its data on a list"""
        
        # Se asume que el archivo tiene la siguiente forma:
        # [S1] 0 1 2 3 4 ..... 108 0 1 2 3 .... 108 1 2 3 ... 108 
        # [S"] .
        # [S2] .
        # [Sk] .
        # [S204] .
        # 
        # En data_source se devuelve una lista (array) de 1x(108*13*204) con el orden: [S1, S2, S3 .... S204]

        #os.path.join(os.path.expanduser('~'), 'documents', 'python', 'file.txt')
        
		with open(file_path, 'r') as f:     # usar with open tiene la ventaja de que automaticamente se cierra el file
			lines = f.read().split()   # devuelve una lista del tipo ['valor1' 'valor2' ....]
		        
        data_source = [float(i) for i in lines] # "converts" the ASCII symbols to their respective floats
        return data_source
	
		# TODO:
		# deberia considerar tenermenos de un cuadro ofdm? por ejemplo del 0 al 107?
		# ver la manera de representar y convertir los float complejos, y la separacion
		# PENSAR MAS TESTS
		# Ver las SP esperadas aux_expected_sp, pensar ya la PRBS
		# Ver la modulación de cada cosa.
		


# Aquí comienza el testing
    def test_sp_ofdm_frame (self):
        """Tests the values in the sp_index. Only tests if SP are in the correct positions"""
        mode = 1
        carriers_number = pow(2, 10+mode)
		file_path = ************
        data_source = self.open_file_and_load_to_list(file_path)
        sp_index = self.aux_get_SP_index(mode)

        # expected_sp = self.aux_expected_sp()
        expected_sp = [0]*len(sp_index) # expect a vector size sp_index filled with zeros 

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

        result_data = dst.data()
        result_sp = numpy.take(result_data, sp_index) # get the elements wich index are the element on sp_index
        self.assertFloatTuplesAlmostEqual(expected_sp, result_sp)
		

		
		
    def test_data_ofdm_frame (self):
        """Check that the data in the OFDM produced (not consider SP, AC, TMCC) has the right structure"""
	        
        mode = 1

        size_by_mode = {1: 96, 2: 192, 3: 384}
        carriers_number = pow(2, 10+mode)
        file_source_path = ***************

		data_source = self.open_file_and_load_to_list(file_path)
		# Si el archivo fuente contiene las TMCC, AC, SP (como puede ser un archivo generado a partir de gr-isdbt),
        # en ese caso se utiliza expected_data = self.aux_get_data(ofdm_frames, mode)
		
        expected_data = data_source

		##########
        # Bloques
        ##########
        src1 = blocks.vector_source_c(data_source, False, size_by_mode[mode]*13)
        dst = blocks.vector_sink_c(carriers_number)
        sqr = isdbt.ofdm_frame_structure(carriers_number)

        ############
        # Conexiones
        ############
        self.tb.connect(src1, sqr)
        self.tb.connect(sqr, dst)
        self.tb.run()

        result_ofdm_frames= dst.data()
        result_data = self.aux_get_data(result_ofdm_frames, mode)
        self.assertFloatTuplesAlmostEqual(expected_data, result_data)
		
		
		
		
	def test_tmcc_ofdm_frame (self):
		mode = 1
		carriers_number = pow(2,10+mode)
		file_path = *************
		data_source = self.open_file_and_load_to_list(file_path)
		
		
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
		
		*** Chequear la alternancia entre los w0 y w1
		el_rango_correspondiente_a_w0y1(result o result_tmcc)
		for i in tmcc_index:
			 (el_rango_correspondiente_a_w0y1(result o result_tmcc) AND BIT A BIT(el de indice i menor)
			si ese and es 0 => OK, paso al siguiente
			si ese and <> 0 => FAIL, retorno ERRROR
		len(tmcc_index)
		****
		
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
		
		
	def test_ac_ofdm_frame (self):
		mode = 1
		carriers_number = pow(2,10+mode)
		file_path = **********
		data_source = self.open_file_and_load_to_list(file_path)
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

		
		
		
		
    def test_001_ofdm_frame (self):
        a = self.aux_expected_tmcc(0,0)
        print a
     #    ###########################################
    	# # Variables
    	# ###########################################
    	# src_segments = []			#define un array 
    	# mode = 1					#modo de transmision
    	# size = 2048		#cantidad total de portadoras, incluyendo las SP,TMCC,AC.
    	# sp_step = 12				#una SP cada 12 portadoras
    	# sp_index = range(0,size,sp_step) #indices absolutos de las SP en un simbolo OFDM (0,12,24.48,...,2040 para modo 1)
    	
    	# tmcc_index_mode1 = 322+(70+11*108, 25+9*108, 17+7*108, 86+5*108, 44+3*108, 47+1*108, 49, 31+2*108, 83+4*108, 61+6*108, 85+8*108, 101+10*108, 23+12*108)
    	# ac1_index_mode1 = 322+(10+11*108, 53+9*108, 61+7*108, 11+5*108, 20+3*108, 74+1*108, 35, 76+2*108, 4+4*108, 40+6*108, 8+8*108, 7+10*108, 98+12*108)
    	# ac2_index_mode1 = 322+(28+11*108, 83+9*108, 100+7*108, 101+5*108, 40+3*108, 100+1*108, 79, 97+2*108, 89+4*108, 89+6*108, 64+8*108, 89+10*108, 101+12*108)

    	# SP = complex(-4.0/3.0, 0)	#Valor constante de la portadora. Debe ser una funcion
    	# expected_result = []
    	# TMCC = -50
    	# AC1 = 999
    	# AC2 = -999
     #    [x+1 for x in mylist]
    	# for i in range(1,14):		#asigna 96 complejos a cada uno de los 13 segmentos
     #    	#src_segments.append([complex(i,i)]*96)
            
     #        src_segments = src_segments + [complex(i,i)]*96 

     #    print("SRC_SEGMENTS")
     #    print(len(src_segments))
        
     #    #Armo el vector esperado
        
     #    expected_result = [0]*322   #Zero-Padding

     #    for i in range(1,14):		#asigna 96 complejos a cada uno de los 13 segmentos
     #    	#expected_result.append([complex(i,i)]*108)
     #    	expected_result = expected_result + [complex(i,i)]*108

     #    expected_result = expected_result + [0]*322 #Zero-Padding

     #    for i in range(0, size):
     #        if i in sp_index:
     #             expected_result[i] = SP
     #        if i in tmcc_index_mode1:
     #             expected_result[i] = TMCC
     #        if i in ac1_index_mode1:
     #             expected_result[i] = AC1
     #        if i in ac2_index_mode1:
     #             expected_result[i] = AC2
     #    filename = "esperado.txt"
     #    file = open(filename, 'w')

     #    for i in range(len(expected_result)):
     #        file.write("%0.1f+%0.1fj || " % (expected_result[i].real, expected_result[i].imag))
     #    file.close()
     #    ###########################################
     #    # Bloques
     #    ###########################################
     #    src1 = blocks.vector_source_c(src_segments, False, 96*13)
     #    dst = blocks.vector_sink_c(size)
     #    sqr = isdbt.ofdm_frame_structure(mode)

     #    ############################################
     #    # Conexiones
     #    ############################################
     #    self.tb.connect(src1, sqr)
     #    self.tb.connect(sqr, dst)
     #    self.tb.run()

     #    result_data = dst.data()

     #    print(expected_result)
     #    print(result_data)

     #    self.assertFloatTuplesAlmostEqual(expected_result, result_data)
if __name__ == '__main__':
    gr_unittest.run(qa_ofdm_frame, "qa_ofdm_frame.xml")