import string

def load_words(file_name):
    print('Loading word list from file...')
    in_file = open(file_name, 'r')
    line = in_file.readline()
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

def is_word(word_list, word):
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'C:\\Users\\vinayak.p\\Desktop\\Python\\ps6\\words.txt'

class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

   
    def get_message_text(self):
        return self.message_text

   
    def get_valid_words(self):
        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        import string
        small_letters=string.ascii_lowercase
        capital_letters=string.ascii_uppercase
        dict={}
        try:
            assert shift > 0 and shift <=26
        except AssertionError:
            pass
        for letter in small_letters:
            result=ord(letter)+shift
            if result > 122:
                result=result-26
            dict[letter]=chr(result)
        for letter in capital_letters:
            result=ord(letter)+shift
            if result > 90:
                result=result-26
            dict[letter]=chr(result)
        return dict
                
            
    def apply_shift(self, shift):
        import string
        small_letters=string.ascii_lowercase
        capital_letters=string.ascii_uppercase
        dict={}
        input=self.message_text
        output=''
        try:
            assert shift > 0 and shift <=26
        except AssertionError:
            pass
        for letter in small_letters:
            result=ord(letter)+shift
            if result > 122:
                result=result-26
            dict[letter]=chr(result)
        for letter in capital_letters:
            result=ord(letter)+shift
            if result > 90:
                result=result-26
            dict[letter]=chr(result)
        for letter in input:
            if letter.isalpha():
                output+=dict[letter]
            else:
                output+=letter
        return output
            
        

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        Message.__init__(self, text)
        self.shift=shift
        self.encrypting_dict=Message.build_shift_dict(self,shift)
        self.message_text_encrypted=Message.apply_shift(self,shift)

    def get_shift(self):
        return self.shift

    def get_encrypting_dict(self):
        return self.encrypting_dict

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        self.shift=shift
        self.encrypting_dict=Message.build_shift_dict(self,shift)
        self.message_text_encrypted=Message.apply_shift(self, shift)

        
class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self, text)
        

    def decrypt_message(self):
        import operator
        data=()
        dict={}
        for i in range(-26,0):
            count=0
            for letter in self.message_text:
                result=Message.apply_shift(self, i)
                if result in Message.get_valid_words(self):
                    count+=1
            dict[abs(i)]=count
        key=26-(max(dict.iteritems(), key=operator.itemgetter(1))[0])
        result=Message.apply_shift(self, key-26)
        data=data+(key,)
        data=data+(result,)
        return data
                
        

#Example test case (PlaintextMessage)
plaintext = PlaintextMessage('hello', 2)
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.get_message_text_encrypted())


#Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq')
print('Expected Output:', (24, 'hello'))
print('Actual Output:', ciphertext.decrypt_message())

#Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('ifmmp')
print('Expected Output:', (25, 'hello'))
print('Actual Output:', ciphertext.decrypt_message())
