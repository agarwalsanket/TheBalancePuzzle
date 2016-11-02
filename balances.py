import turtle
import os
__author__ = "Sanket Agarwal"

"""
This program is the implementation of the problem stated in HW7.
Authors: Sanket Agarwal (sa3250@rit.edu)
"""


class Beam:
    """
    Beam class contains data about a beam.
    """
    __slots__ = 'beam', 'beam_name_objects', 'beam_draw'

    def __init__(self, li_beam, draw):
        """
        Constructor for the Beam class.
        :param li_beam: list of constituent weights/beams for a particular beam.
        :param draw: flag which controls if a beam is to be drawn (=true) or not (=false)
        """
        self.beam = {}
        self.beam_draw = {}
        if draw == 'false':
            self.makebeam(li_beam)
        elif draw == 'true':
            self.makebeam_draw(li_beam)
        else:
            print("improper inputs")

    def makebeam(self, li_beam):
        """
        This function creates a beam object if it is part of a bigger beam.
        :param li_beam: list of constituent weights/beams for a particular beam.
        :return: None
        """
        if li_beam is []:
            return None
        beam_name = li_beam.pop(0)
        count = 0
        for i in range(len(li_beam)):
            self.beam[li_beam[i + count]] = li_beam[i + 1 + count]
            count += 1
            if (i + count + 1) > (len(li_beam) - 1):
                self.beam["name"] = beam_name
                break

    def makebeam_draw(self, li_beam):
        """
        This function creates a beam object so that it can be drawn later.
        :param li_beam: list of constituent weights/beams for a particular beam.
        :return: None
        """
        if li_beam is []:
            return None
        beam_name_draw = li_beam.pop(0)
        count = 0
        for i in range(len(li_beam)):
            self.beam_draw[li_beam[i + count]] = li_beam[i + 1 + count]
            count += 1
            if (i + count + 1) > (len(li_beam) - 1):
                self.beam_draw["name"] = beam_name_draw
                break

    @staticmethod
    def weight(beam):
        """
        This function computes the weight of a beam.
        :param beam: Beam object whose weight is to be computed.
        :return: Weight of the beam object.
        """
        sum_weight = 0
        for k in beam:
            if k != 'name':
                sum_weight += int(beam[k])
        return sum_weight

    def draw(self, name_dict_dict, beams_list, absent_weight, unit_v, unit, t):
        """
        This is the function to be invoked for the drawing of beam.
        :param name_dict_dict: A dictionary of dictionaries containing data about beam.
        :param beams_list: A list of dictionaries containing data about beam.
        :param absent_weight: Missing weight
        :param unit_v: Length of vertical beam.
        :param t: Turtle object
        :return: None
        :pre: (0,0) relative facing East, pen up
        :post: (0,0) relative facing East, pen up
        """

        writable_unit = 30
        reverse_beams_list = beams_list[::-1]
        t.penup()
        t.left(90)
        t.pendown()
        t.forward(-unit_v)
        t.penup()
        t.right(90)
        for i in range(len(reverse_beams_list)):
            for k in reverse_beams_list[i]:
                if k != 'name':
                    t.pendown()
                    t.forward(int(k) * unit)
                    t.penup()
                    if reverse_beams_list[i][k] in name_dict_dict:
                        self.draw(name_dict_dict, [name_dict_dict[reverse_beams_list[i][k]]], absent_weight,
                                  unit_v * 1.5, unit/3, t)
                        t.penup()
                        t.left(90)
                        t.forward(1.5 * unit_v)
                        t.right(90)
                        t.forward(-(int(k) * unit))

                    elif int(reverse_beams_list[i][k]) == -1:
                        reverse_beams_list[i][k] = absent_weight
                        t.left(90)
                        t.pendown()
                        t.backward(unit_v)
                        t.penup
                        t.backward(writable_unit)
                        t.pendown()
                        t.write(reverse_beams_list[i][k], font=("Arial", 12, "bold"))
                        t.penup()
                        t.forward(unit_v + writable_unit)
                        t.right(90)
                        t.forward(-(int(k) * unit))
                    else:
                        t.left(90)
                        t.pendown()
                        t.backward(unit_v)
                        t.penup
                        t.backward(writable_unit)
                        t.pendown()
                        t.write(reverse_beams_list[i][k], font=("Arial", 12, "bold"))
                        t.penup()
                        t.forward(unit_v + writable_unit)
                        t.right(90)
                        t.forward(-(int(k) * unit))
            break


class Weight:
    """
    Weight class to compute torque and missing weights for a beam.
    """
    __slots__ = 'weight', 'beam_name_dict_with_obj', 'beam_dict_list', 'name_dict_dict', 'absent_weight'

    def __init__(self, beam_name_dict_with_obj, beam_dict_list, name_dict_dict):
        """
        Constructor function for the Weight class.
        :param beam_name_dict_with_obj: Dictionary of dictionaries containing data of beam.
        :param beam_dict_list: A list of dictionaries containing data about beam.
        :param name_dict_dict: Dictionary of dictionaries containing data of beam.
        """
        self.beam_dict_list = beam_dict_list
        self.beam_name_dict_with_obj = beam_name_dict_with_obj
        self.name_dict_dict = name_dict_dict
        self.absent_weight = 0
        self.balance()

    def balance(self):
        """
        Function to compute whether a beam is balanced or not, and if not, to compute the missing weight.
        :return: None
        """
        for i in range(len(self.beam_dict_list)):
            calculate_balance = 'true'
            balance = 0
            for k in self.beam_dict_list[i]:
                if k != 'name':
                    if self.beam_dict_list[i][k] in self.beam_name_dict_with_obj:
                        self.beam_dict_list[i][k] = Beam.weight(self.beam_name_dict_with_obj.get(
                            self.beam_dict_list[i][k]).beam)

                    if int(self.beam_dict_list[i][k]) == -1:
                        k_temp = k
                        balance = 0
                        temp = i
                        partial_sum_weight = 0
                        print("The beam " + self.beam_dict_list[temp][
                            'name'] + " has an empty pan, at distance " + k_temp)
                        for k in self.beam_dict_list[temp]:
                            if k != 'name' and self.beam_dict_list[temp][k] != '-1':

                                if self.beam_dict_list[temp][k] in self.beam_name_dict_with_obj:
                                    self.beam_dict_list[temp][k] = Beam.weight(self.beam_name_dict_with_obj.get(
                                        self.beam_dict_list[temp][k]).beam)
                                partial_sum_weight += int(k) * int(self.beam_dict_list[temp][k])
                        self.beam_dict_list[temp][k_temp] = str(-partial_sum_weight // int(k_temp))
                        self.absent_weight = self.beam_dict_list[temp][k_temp]
                        print("It should be filled with weight of " + self.beam_dict_list[temp][
                            k_temp] + " units to be balanced. Now " + self.beam_dict_list[temp][
                                  'name'] + " will also be balanced")
                        break
                    if calculate_balance != 'false':
                        balance += int(k) * int(self.beam_dict_list[i][k])

            if balance == 0:
                print(self.beam_dict_list[i]['name'] + ' is balanced')
            else:
                print(self.beam_dict_list[i]['name'] + ' is not balanced')

        for i in range(len(self.beam_dict_list)):
            for k in self.beam_dict_list[i]:
                if self.beam_dict_list[i][k] in self.beam_name_dict_with_obj:
                    self.beam_dict_list[i][k] = self.beam_name_dict_with_obj.get(self.beam_dict_list[i][k])


def main():
    """
    Main function of the implementation.
    :return: None
    """
    while 1:
        file_puzzle = input("Enter the file name having the description of the Balance Puzzle ")
        if not os.path.isfile(file_puzzle):
            print("File does not exist")
        else:
            break
    beams_name_obj_dict = {}
    name_beam_dict = {}
    beams_list = []
    beams_name_obj_dict_draw = {}
    name_beam_dict_draw = {}
    beams_list_draw = []

    with open(file_puzzle) as beam:
        for line in beam:
            li_beam_local = line.split()
            if len(li_beam_local) % 2 == 0:
                print("Invalid entries in line ", li_beam_local)
            lextent = 0
            rextent = 0
            li_name = li_beam_local[0]
            li_temp = li_beam_local[1::2]
            for i in range(len(li_temp)):
                if int(li_temp[i]) < lextent:
                    lextent = int(li_temp[i])
                if int(li_temp[i]) > rextent:
                    rextent = int(li_temp[i])
            beam = Beam(li_beam_local, 'false')
            beams_name_obj_dict[line.split()[0]] = beam
            name_beam_dict[line.split()[0]] = beam.beam
            beams_list.append(beam.beam)
            print("Length of beam ", li_name, "is: ", (abs(lextent) + abs(rextent)))
            print("Left extent of beam ", li_name, "is: ", lextent, " and the right extent is: ", rextent)

    with open(file_puzzle) as beam:
        for line in beam:
            li_beam_local_draw = line.split()
            beam_draw = Beam(li_beam_local_draw, 'true')
            beams_name_obj_dict_draw[line.split()[0]] = beam_draw
            name_beam_dict_draw[line.split()[0]] = beam_draw.beam_draw
            beams_list_draw.append(beam_draw.beam_draw)

    wt = Weight(beams_name_obj_dict, beams_list, name_beam_dict)
    beam_draw.draw(name_beam_dict_draw, beams_list_draw, wt.absent_weight, 10, 30, turtle)
    turtle.exitonclick()


if __name__ == "__main__":
    main()
