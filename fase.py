# -*- coding: utf-8 -*-
from itertools import chain
from os import path
import sys

project_dir = path.dirname(__file__)
project_dir = path.join('..')
sys.path.append(project_dir)

from atores import *
ator=__import__('atores')

VITORIA = 'VITORIA'
DERROTA = 'DERROTA'
EM_ANDAMENTO = 'EM_ANDAMENTO'


class Ponto():
    def __init__(self, x, y, caracter):
        self.caracter = caracter
        self.x = round(x)
        self.y = round(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.caracter == other.caracter

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self, *args, **kwargs):
        return "Ponto(%s,%s,'%s')" % (self.x, self.y, self.caracter)


class Fase():
    def __init__(self, intervalo_de_colisao=1):
        """
        Método que inicializa uma fase.

        :param intervalo_de_colisao:
        """
        self.intervalo_de_colisao = intervalo_de_colisao
        self._passaros = []
        self._porcos = []
        self._obstaculos = []


    def adicionar_obstaculo(self, *obstaculos):
        """
        Adiciona obstáculos em uma fase

        :param obstaculos:
        """
        return self._obstaculos.extend(obstaculos)

    def adicionar_porco(self, *porcos):
        """
        Adiciona porcos em uma fase

        :param porcos:
        """
        return self._porcos.extend(porcos)

    def adicionar_passaro(self, *passaros):
        """
        Adiciona pássaros em uma fase

        :param passaros:
        """
        return self._passaros.extend(passaros)

    def status(self):
        """
        Método que indica com mensagem o status do jogo

        Se o jogo está em andamento (ainda tem porco ativo e pássaro ativo), retorna essa mensagem.

        Se o jogo acabou com derrota (ainda existe porco ativo), retorna essa mensagem

        Se o jogo acabou com vitória (não existe porco ativo), retorna essa mensagem

        :return:
        """
        if not self._checar_porcos() or self._checar_passaros():
            return VITORIA
        elif self._checar_passaros()and self._checar_porcos():
            return EM_ANDAMENTO
        elif not self._checar_passaros() or self._checar_porcos():
            return DERROTA



    def _checar_atores(self, lista_atores):
        for ator in lista_atores:
            if ator.caracter:
                return True
        return False

    def _checar_porcos(self):
        return self._checar_atores(self._porcos)

    def _checar_passaros(self):
        return self._checar_atores(self._passaros)


    def lancar(self,angulo,tempo):
        """
        Método que executa lógica de lançamento.

        Deve escolher o primeiro pássaro não lançado da lista e chamar seu método lançar

        Se não houver esse tipo de pássaro, não deve fazer nada

        :param angulo: ângulo de lançamento
        :param tempo: Tempo de lançamento
        """
        #if self._checar_passaros() in any(self._passaros):
        #    return ator._passaros.lancar(self,angulo,tempo)
        for passaro in self._passaros:
            if not passaro.foi_lancado():
               return passaro.lancar(angulo, tempo)


    def calcular_pontos(self, tempo):
        """
        Lógica que retorna os pontos a serem exibidos na tela.

        Cada ator deve ser transformado em um Ponto.

        :param tempo: tempo para o qual devem ser calculados os pontos
        :return: objeto do tipo Ponto
        """
        pontos=[]
        for ator in (self._passaros+self._obstaculos+self._porcos):
            pontos.append(self._transformar_em_ponto(ator))
        return pontos

    def ponto_passaro(self, passaro,tempo):
        passaro.calcular_posicao(tempo)
        for ator in chain(self._obstaculos, self._porcos):
            if passaro.status():
                passaro.colidir(ator, self.intervalo_de_colisao)
                passaro.colidir_com_chao()
                self._transformar_em_ponto(passaro)
            else:
                break
        return self._transformar_em_ponto(passaro)

    def _transformar_em_ponto(self, ator):
        return Ponto(ator.x, ator.y, ator.caracter())
