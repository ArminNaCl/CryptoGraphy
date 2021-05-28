import argparse
from cryptography.fernet import Fernet

class Key:
    def __init__(self):
        pass

    def generate(self,file=None):
        """
            generate a key and save it in the file 
        """
        key = Fernet.generate_key()
        if file == None:
            return key
        with open(file,'xb')as k:
            k.write(key)

    def get_key_str(self,str):
        return Fernet(str)

    def get_key_file(self,file):
        with open(file,'r') as k:
            str = k.read()
        return Fernet(str)
    
class CryptInterface:
    def __init__(self) -> None:
        pass

    def text(self):
        pass

    def file(self):
        pass

class EnCrypt(CryptInterface):
    def __init__(self):
        pass

    def text(self, plane:str, key:str) ->bytes :
        """   
            encrypt a plane with a key and return the encrypted file in bytes
        """
        return key.encrypt(str.encode(plane))

    def file(self, file:str, key:Key, save=None) -> None:
        """   
            encrypt a file with the key and return nothing
        """
        with open(file,'rb') as f:
            plane=f.read()
        cypher =  key.encrypt(plane).decode()
        if save:
            with open(save,'x') as f:
                f.write(cypher)
        else: return cypher


class DeCrypt(CryptInterface):
    def __init__(self):
        pass

    def text(self,cypher:bytes,key:str)->str:
        """
            decrypt a cypher with the key and return it in plane
        """
        return key.decrypt(cypher).decode()

    def file(self,file:str,key:str,save=None)->None:
        """
            decrypt a file with the key and return nothing
        """
        with open(file,'rb') as f:
            cypher=f.read()
        plane = key.decrypt(cypher)
        if save:
            with open(save,'xb') as f:
                f.write(plane) 
        else: return plane

class CryptFactory:
    @staticmethod
    def getCrypt(type:str)->object:
        type =type.lower()
        if type =='decrypt':
            return DeCrypt()
        elif type == 'encrypt':
            return EnCrypt()
        else:
            assert False , "decrypt or encrypt"



                


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Cryptography util script.')
    subparser = parser.add_subparsers(dest='command')
    decrypt_parser = subparser.add_parser('decrypt')
    encrypt_parser = subparser.add_parser('encrypt')
    key_parser = subparser.add_parser('generate_key')
    subparser.add_parser('help')


    decrypt_parser.add_argument('file', metavar='PATH',
                    action='store', help='path to target file.')
    decrypt_parser.add_argument('-k', '--key', action='store',
                    help='fernet key to decrypt')
    decrypt_parser.add_argument('-K', '--key-path', 
                    action='store', help='path to fernet key')
    decrypt_parser.add_argument('-s', '--save',
                    action='store', help='path to save (optional)')

    encrypt_parser.add_argument('file', nargs='?', metavar='PATH',
                    action='store', help='path to target file.')
    encrypt_parser.add_argument('-k', '--key', action='store',
                    help='fernet key to encrypt (Default: generate new)')
    encrypt_parser.add_argument('-K', '--key-path', 
                    action='store', help='path to fernet key')
    encrypt_parser.add_argument('-s', '--save', metavar='PATH',
                    action='store', help='path to save (optional)')

    key_parser.add_argument('-s', '--save', action='store', help='path to save (optional)')

    args = parser.parse_args()

    print(args)


    c = CryptFactory()
    k =Key()
    if args.command == 'generate_key':
        k=k.generate(args.save)
        if k:
            print('key is:',k)
    elif args.command in ['encrypt','decrypt']:
        c = c.getCrypt(args.command)
        if args.key_path:
            key = k.get_key_file(args.key_path)
        elif args.key:
            key = k.get_key_str(args.key)
        else :
            raise Exception('key is required')
        c.file(args.file,key,args.save)
    else:
        parser.print_help()
    


    