import functools
import operator as op


BYTE_SIZE: int = 8
MAX_1_BYTE: int = 0b_11111111


class Ip:
    @classmethod
    def from_dec_str(
            cls,
            dec_repr
        ) -> 'Ip':
        """
        Constructeur à partir de la représentation décimale d'une ip.
        :param dec_repr: La représentation décimale pointée de l'ip.
        """
        ip = Ip()
        ip.dec_repr_str = dec_repr
        return ip

    def __init__(self) -> None:
        """
        Constructeur.
        """
        self._id: int = 0
    
    @property
    def dec_repr_str(self) -> str:
        """Assesseur de la représentation décimale pointée de l'adresse ip."""
        return '.'.join([
            str((self._id >> (i * BYTE_SIZE)) & MAX_1_BYTE)
            for i in reversed(range(4))
        ])
    
    @dec_repr_str.setter
    def dec_repr_str(
            self,
            dec_repr: str
        ) -> 'Ip':
        """
        Modificateur de la représentation décimale pointée de l'adresse ip.
        """
        self._id = functools.reduce(
            op.or_,
            [
                int(str_digit) << (d * BYTE_SIZE)
                for d, str_digit in enumerate(reversed(dec_repr.split('.')))
            ]
        )