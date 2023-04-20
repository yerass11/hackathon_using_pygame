"""This module implements sprite animations for Floor-jumper"""
# Этот код определяет класс под названием Animation, 
# который используется для реализации логики анимации для спрайтов. 
# Класс имеет четыре переменные экземпляра:

# animate: последовательность целых чисел, 
# которые являются индексами списка изображений внешнего спрайта.
# frames_per_update: количество кадров, которые необходимо дождаться,
# прежде чем будет обновлен текущий индекс в списке последовательностей.
# frames_delayed: счетчик, который отслеживает, сколько кадров было отложено с момента последнего обновления.
# current_frame_index: какой кадр в списке последовательностей отображается в данный момент.
# Класс имеет четыре метода:

# __init__(self, frame_sequence, delay):
#     инициализирует переменные экземпляра с заданными frame_sequence и delay.
# get_current_frame(self): 
#     возвращает текущий кадр для рендеринга, который является текущим кадром в последовательности анимации.
# reset (self): 
#     сбрасывает внутреннее состояние анимации.
# animate (self): 
#     обновляет текущий кадр, если это необходимо, или обновляет внутреннее состояние. 
#     Этот метод должен вызываться один раз за кадр при анимации. 
#     Если счетчик frames_delayed больше значения frames_per_update, 
#     обновляется current_frame_index и счетчик frames_delayed сбрасывается на ноль. 
#     Если current_frame_index выходит за пределы длины списка анимации, 
#     он сбрасывается на 0. В противном случае счетчик frames_delayed увеличивается на 1.




class Animation():
    """Implements animation logic for sprites, this is really just a list of ints - simple"""

    def __init__(self, frame_sequence, delay):
        """Initialize the animation object"""

        # Sequence of ints that are indicies to the external sprite's image list
        self.animation = frame_sequence
        # Assuming Animation.animate() is called once per frame, this is the number
        # of frames before the current index to the sequence list is updated
        self.frames_per_update = delay
        # counter to track when to update the current fram
        self.frames_delayed = 0
        # Which frame in the sequence (list) are we currently showing
        self.current_frame_index = 0
        
    def get_current_frame(self):
        """Returns the frame to render, e.g. the current frame in the animation sequence"""
        return self.animation[self.current_frame_index]

    def reset(self):
        """Reset internal state"""
        self.current_frame_index = 0
        self.frames_delayed = 0

    def animate(self):
        """Update the current frame if needed, or update internal state, 
        should be called once per frame when animating"""
        if self.frames_delayed > self.frames_per_update:
            self.frames_delayed = 0
            self.current_frame_index += 1
            if self.current_frame_index > len(self.animation) - 1:
                self.current_frame_index = 0
        else:
            self.frames_delayed += 1