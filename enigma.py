#!/bin/python

import argparse

description = \
"""This emulator will encode and decode messages based on the
Enigma IV Cipher Machine manufactured by Creative Crafthouse in Hudson, FL USA

http://www.creativecrafthouse.com/index.php?main_page=product_info&products_id=977

Example usage:
  decode:
  ./enigma.py decode EMC 506172 -m 'GWVP LOMU HPZY VOUA SZVJ V!'

  encode:
  ./enigma.py encode EMC 506172 -m 'The moon is made of cheese!'

"""

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=description)
parser.add_argument('process', help="either 'encode' OR 'decode'")
parser.add_argument("keyphrase", help="the 3 letter keyphrase e.x. EMC")
parser.add_argument("wheel_order", help="the 6 digit wheel order e.x. 506172")
parser.add_argument("-m", "--message", help="the text message to be processed e.x. 'The moon is made of cheese!'")
args = parser.parse_args()

''' Wheel class used set/get wheel properties '''
class Wheel(object):

  def setAlphabet(self, alphabet):
    self.alphabet = alphabet

  def printAlphabet(self):
    print(self.alphabet)

  def setOffset(self, offset):
    self.offset = offset

  def printOffsetIndex(self):
    print(self.offset)

  def printOffsetLetter(self):
    print(self.alphabet[self.offset])

''' These are the encoding wheels with randomized alphabets. '''
alphabets = {
'50':'XGBRCJSQIEFTVHYAPOWZNULKMD',
'51':'REHKVMQTFSJNXBWZGDOALCUPIY',
'52':'SUBWDVRFMKHPOLZCGXINQAJEYT',
'53':'YOBEZALKIHRCUFVQWTSMPXGNJD',
'60':'VIWNXUPTCRHJMBZYAKDOLQSEGF',
'61':'DUSYOCQGZALBKFWHJIVEMPXRNT',
'62':'DASQOPELGKUVBTWYRCINHMXJFZ',
'63':'ZFTIKGOPJLYUDHNMAWVSRECXBQ',
'70':'OSADNJLUXCRQZTHEVBGFYIPKWM',
'71':'INFEGJBTMPZSQWUYKRXHCDLVOA',
'72':'OZBNXIALJFRWGKQCDVYMTEUSHP',
'73':'XGWMOVIZDEFYSPBRTJHAQCKULN'
}

''' Set up the initial machine state '''
# wheel order as a single string of digits
wheel_order = args.wheel_order

# array of wheel objects
wheels = []

if (wheel_order.isnumeric()):
  ''' use list comprehension to split the wheel names into an iterable list '''
  j = 0
  # split the wheel order parameter into groups of 2 digits
  n = 2
  for wheel_name in [wheel_order[j:j+n] for j in range(0, len(wheel_order), n)]:
    try:
      wheel = Wheel()
      wheel.setAlphabet(alphabets[wheel_name])
      wheels.append(wheel)
    except:
      print(wheel_name,"is not a valid wheel.")
      exit();

''' Arrange wheels according to keyphrase '''
# keyphrase to set initial wheel position
keyphrase = args.keyphrase
if (keyphrase.isalpha()):
  i = 0
  for c in keyphrase:
    wheels[i].setOffset(wheels[i].alphabet.index(c))
    i += 1

''' Encode function
    Loop through the plain text message and encode it '''
def encodeMessage(plain_text):
  encoded_text = ''
  j = 1

  plain_text = plain_text.upper().replace(' ', '')

  for l in plain_text:
    ''' Pass non-alpha characters '''
    if (l.isalpha()):

      ''' Alternate encoding wheels and get offset. '''
      if (j % 2):
        encoder_offset = wheels[0].alphabet.index(l) - wheels[0].offset
      else:
        encoder_offset = wheels[1].alphabet.index(l) - wheels[1].offset

      ''' Rollover to treat wheel as a physical circle '''
      if (encoder_offset + wheels[2].offset > len(wheels[2].alphabet) - 1):
        encoder_offset = encoder_offset + wheels[2].offset - len(wheels[2].alphabet)
        encoded_text += wheels[2].alphabet[encoder_offset]
      else:
        encoded_text += wheels[2].alphabet[wheels[2].offset + encoder_offset]

      ''' Space the encoded message in groups of 4 '''
      if (j % 4 == 0):
        encoded_text += ' '

    else:
      encoded_text += l

    j += 1

  print('encoded text:', encoded_text)

''' Decode function '''
def decodeMessage(encoded_text):
  decoded_text = ''
  j = 1

  encoded_text = encoded_text.upper().replace(' ', '')

  for l in encoded_text:
    ''' Pass non-alpha characters '''
    if (l.isalpha()):
      decoder_offset = wheels[2].alphabet.index(l) - wheels[2].offset

      ''' Alternate decoding wheels with appropriate offset and rollover. '''
      if (j % 2):
        if (decoder_offset + wheels[0].offset > len(wheels[0].alphabet) - 1):
          decoder_offset += wheels[0].alphabet[decoder_offset]
          decoded_text += wheels[0].alphabet[decoder_offset]

        else:
          decoded_text += wheels[0].alphabet[decoder_offset + wheels[0].offset]

      else:
        if (decoder_offset + wheels[1].offset > len(wheels[1].alphabet) - 1):
          decoder_offset += wheels[1].alphabet[decoder_offset]
          decoded_text += wheels[1].alphabet[decoder_offset]

        else:
          decoded_text += wheels[1].alphabet[decoder_offset + wheels[1].offset]

    else:
       decoded_text += l

    j += 1

  print('decoded text:', decoded_text)

if (args.process == 'encode' and args.message):
  encodeMessage(args.message)
else:
  decodeMessage(args.message)
