import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Giris
noise = ctrl.Antecedent(np.arange(0, 101, 1), 'noise')  
time_of_day = ctrl.Antecedent(np.arange(0, 25, 1), 'time_of_day')  
session_duration = ctrl.Antecedent(np.arange(0, 181, 1), 'session_duration')  
distractions = ctrl.Antecedent(np.arange(0, 11, 1), 'distractions')  
mood = ctrl.Antecedent(np.arange(0, 11, 1), 'mood')  

#  Cikis 
music_mode = ctrl.Consequent(np.arange(0, 101, 1), 'music_mode')
break_suggestion = ctrl.Consequent(np.arange(0, 101, 1), 'break_suggestion')


noise['silent'] = fuzz.trimf(noise.universe, [0, 0, 40])
noise['medium'] = fuzz.trimf(noise.universe, [30, 50, 70])
noise['noisy'] = fuzz.trimf(noise.universe, [60, 100, 100])

time_of_day['morning'] = fuzz.trimf(time_of_day.universe, [5, 8, 11])
time_of_day['day'] = fuzz.trimf(time_of_day.universe, [10, 14, 18])
time_of_day['evening'] = fuzz.trimf(time_of_day.universe, [17, 20, 23])
time_of_day['night'] = fuzz.trimf(time_of_day.universe, [0, 3, 6])

session_duration['small'] = fuzz.trimf(session_duration.universe, [0, 0, 60])
session_duration['medium'] = fuzz.trimf(session_duration.universe, [45, 90, 135])
session_duration['long'] = fuzz.trimf(session_duration.universe, [120, 180, 180])

distractions['few'] = fuzz.trimf(distractions.universe, [0, 0, 3])
distractions['medium'] = fuzz.trimf(distractions.universe, [2, 5, 8])
distractions['lot'] = fuzz.trimf(distractions.universe, [7, 10, 10])

mood['tired'] = fuzz.trimf(mood.universe, [0, 0, 4])
mood['normal'] = fuzz.trimf(mood.universe, [3, 5, 7])
mood['energetic'] = fuzz.trimf(mood.universe, [6, 10, 10])

music_mode['silence'] = fuzz.trimf(music_mode.universe, [0, 0, 40])
music_mode['soft_music'] = fuzz.trimf(music_mode.universe, [30, 50, 70])
music_mode['white_noise'] = fuzz.trimf(music_mode.universe, [60, 100, 100])

break_suggestion['keep_going'] = fuzz.trimf(break_suggestion.universe, [0, 0, 30])
break_suggestion['break_soon'] = fuzz.trimf(break_suggestion.universe, [20, 50, 80])
break_suggestion['take_a_break'] = fuzz.trimf(break_suggestion.universe, [70, 100, 100])

rules = [
    ctrl.Rule(noise['silent'] & mood['energetic'], music_mode['silence']),
    ctrl.Rule(noise['silent'] & mood['tired'], music_mode['soft_music']),
    ctrl.Rule(noise['medium'] & mood['normal'], music_mode['soft_music']),
    ctrl.Rule(noise['noisy'] & mood['normal'], music_mode['white_noise']),
    ctrl.Rule(noise['noisy'] & mood['tired'], music_mode['white_noise']),
    ctrl.Rule(time_of_day['night'] & mood['tired'], music_mode['silence']),
    ctrl.Rule(time_of_day['day'] & noise['noisy'], music_mode['white_noise']),
    ctrl.Rule(time_of_day['morning'] & mood['energetic'], music_mode['soft_music']),
    ctrl.Rule(distractions['lot'], music_mode['white_noise']),
    ctrl.Rule(distractions['few'] & noise['silent'], music_mode['silence']),

    ctrl.Rule(session_duration['small'] & mood['energetic'], break_suggestion['keep_going']),
    ctrl.Rule(session_duration['long'] | distractions['lot'], break_suggestion['take_a_break']),
    ctrl.Rule(session_duration['medium'] & mood['normal'], break_suggestion['break_soon']),
    ctrl.Rule(mood['tired'], break_suggestion['take_a_break']),
    ctrl.Rule(mood['normal'] & distractions['medium'], break_suggestion['break_soon']),
    ctrl.Rule(mood['energetic'] & distractions['few'], break_suggestion['keep_going']),
    ctrl.Rule(time_of_day['night'] & session_duration['long'], break_suggestion['take_a_break']),
    ctrl.Rule(time_of_day['day'] & distractions['lot'], break_suggestion['break_soon']),
    ctrl.Rule(time_of_day['evening'] & mood['tired'], break_suggestion['take_a_break']),
    ctrl.Rule(time_of_day['morning'] & mood['energetic'], break_suggestion['keep_going']),
    ctrl.Rule(session_duration['small'] & distractions['few'], break_suggestion['keep_going']),
    ctrl.Rule(session_duration['medium'] & distractions['lot'], break_suggestion['take_a_break']),
    ctrl.Rule(session_duration['long'] & mood['normal'], break_suggestion['break_soon']),
    ctrl.Rule(mood['energetic'] & distractions['medium'], break_suggestion['break_soon']),
    ctrl.Rule(time_of_day['evening'] & session_duration['medium'], break_suggestion['break_soon']),
    ctrl.Rule(time_of_day['morning'] & session_duration['small'], break_suggestion['keep_going']),
    ctrl.Rule(time_of_day['night'] & mood['normal'], break_suggestion['break_soon']),

]

focus_ctrl = ctrl.ControlSystem(rules)


def analyze_focus(noise_val, time_val, session_val, distraction_val, mood_val):
    simulator = ctrl.ControlSystemSimulation(focus_ctrl)

    simulator.input['noise'] = noise_val
    simulator.input['time_of_day'] = time_val
    simulator.input['session_duration'] = session_val
    simulator.input['distractions'] = distraction_val
    simulator.input['mood'] = mood_val

    simulator.compute()

    music = simulator.output['music_mode']
    rest = simulator.output['break_suggestion']
    
    def interpret_music(val):
        if val <= 35:
            return ("sessizlik",
                    "Ortam sessiz, dikkat dağıtıcı olmadan işinize veya dersinize odaklanabilirsiniz.")
        elif val <= 65:
            return ("yumuşak müzik",
                    "Arka planda sakin ve hafif bir müzik çalıyor. Rahatlamanıza ve konsantrasyonunuzu artırmanıza yardımcı olabilir.")
        else:
            return ("beyaz gürültü",
                    "Beyaz gürültü çalıyor — dış sesleri maskelemek ve gürültülü ortamda konsantrasyonu artırmak için uygundur.")

    def interpret_break(val):
        if val <= 30:
            return ("devam edebilirsiniz",
                    "Formdasınız, çalışmaya devam edin. Yakın zamanda ara vermenize gerek yok.")
        elif val <= 70:
            return ("mola yakında",
                    "Yakında kısa bir mola vermeniz gerekiyor gibi görünüyor. Güç toplamak için hazırlanın.")
        else:
            return ("dinlenme zamanı",
                    "Şimdi ara vermeniz şiddetle tavsiye edilir. Dinlenerek verimliliğinizi artırabilir ve yorgunluğu azaltabilirsiniz.")


    return interpret_music(music), interpret_break(rest)
