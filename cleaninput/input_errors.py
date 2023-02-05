import logging

class InputErrors():

    def __init__(self):
        self.error_list = []

    def append(self, index: int, column:str):
        self.error_list.append([index,column])



if __name__ == '__main__':
    '''test getting the number of compettitors '''
    ie=InputErrors()
    ie.append(1,"Age")
    ie.append(33,"Height")
    ie.append(35,"Weight")

    logging.info(ie.error_list)
    for i in range(len(ie.error_list)):
        logging.info(ie.error_list[i][1])

