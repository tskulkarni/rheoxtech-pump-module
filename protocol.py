import array

class Protocol:
    def __init__(self,ser_handle):
        self.ser_handle = ser_handle

    def CHAR_HEX(self, c:str):
        if c > '9':
            return(ord(c) - ord('A')+ 0x0A)
        else:
            return(ord(c)-0x30)

    #Single Hex nibble to its ASCII character conversion
    def HEX_CHAR(self,h):
        return("0123456789ABCDEF"[h])


    def ASCII_TO_HEX(self,ascii_buf):
        msn = ascii_buf[0].upper()
        lsn = ascii_buf[1].upper()
        value = self.CHAR_HEX (ascii_buf[0].upper())
        value = value << 4
        value += self.CHAR_HEX (ascii_buf[1].upper())
        return value

    def HEX_TO_ASCII(self,byte):
        ascii_buff=""
        ascii_buff+=  self.HEX_CHAR((byte >> 4) & 0x0F)
        ascii_buff+=  self.HEX_CHAR(byte & 0x0F)
        return ascii_buff

    def makecmd(self, cmd_code, data):
        out_cmd=""
        out_cmd +=f':0{cmd_code}'
        data_len=len(data)
        out_cmd +=self.HEX_TO_ASCII(data_len)
        for d in data:
            out_cmd +=self.HEX_TO_ASCII(d)
        crc = 0
        for i in out_cmd[1:]:
            crc += ord(i)
        crc = crc & 0xFF
        crc = (~crc & 0xFF)+1
        out_cmd += self.HEX_TO_ASCII(crc)
        out_cmd += "\r\n"
        return out_cmd

    def check_rsp(self, rsp):
        hex_bytes = bytearray()
        index = 1
        #return hex_bytes
        while index < len(rsp)-2:
            hex_value = self.ASCII_TO_HEX(rsp[index:index+2])
            hex_bytes.append(hex_value)
            index = index + 2
        error_code = hex_bytes[0]
        data_length = hex_bytes[1]
        #print(f'Error: {error_code}, Data_length: {data_length}')
        if data_length:
            decoded = array.array('I',hex_bytes[2:2+data_length])
            #print(f'Reveived Data {decoded}')
            return decoded
        return None

    def get_param(self, motor_mask, param_code):
        cmd = self.makecmd('G', [motor_mask, param_code])
        self.ser_handle.write(cmd.encode('utf-8'))
        resp = ""
        resp = self.ser_handle.readline()
        resp = resp.decode('utf-8')
        #print(f"Data RX: {resp}")
        data_received = self.check_rsp(resp)
        #print(f'Parameter Data {data_received}')
        return data_received

    def put_param(self, motor_mask, param_code, param_value):
        param_bytes = param_value.to_bytes(4, byteorder='little')
        cmd_data = [motor_mask, param_code]
        cmd_data = cmd_data + list(param_bytes)
        cmd = self.makecmd('P', cmd_data)
        self.ser_handle.write(cmd.encode('utf-8'))
        resp=""
        resp = self.ser_handle.readline()
        resp=resp.decode('utf-8')
        #print(f"Data RX: {resp}")
        data_received = self.check_rsp(resp)
        #print(f'Parameter Data {data_received}')

    def execute_cmd(self, motor_mask, command_code,direction=None, speed_steps_p_sec=None):
        cmd_data = [motor_mask]
        if direction is not None:
            dir_bytes = direction.to_bytes(4, byteorder='little')
        else:
            dir_bytes = b''
        if speed_steps_p_sec is not None:
            speed_bytes = speed_steps_p_sec.to_bytes(4, byteorder='little')
        else:
            speed_bytes = b''
        cmd_data = cmd_data + list(dir_bytes) + list(speed_bytes)
        print(f'{cmd_data=}')
        cmd = self.makecmd(command_code, cmd_data)
        self.ser_handle.write(cmd.encode('utf-8'))
        resp=""
        resp = self.ser_handle.readline()
        resp=resp.decode('utf-8')
        #print(f"Data RX: {resp}")
        #data_received = self.check_rsp(resp)
        #print(f'Parameter Data {data_received}')
