import time
import faker, random
from faker_e164.providers import E164Provider
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#import selenium action chains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from state_abbrev import us_state_to_abbrev
from email_data import *
from signature import *
from handwriting_synthesis import Hand
from svg.path import parse_path, Move, Path
from xml.dom import minidom

url = "https://fs7.formsite.com/DyGKwz/eguau648q8/index"
fake = faker.Faker()
fake.add_provider(E164Provider)

all_fields = {
    "RSVP": ['RESULT_CheckBox-0_0', 'RESULT_CheckBox-0_1'],
    #Select
    "Pronouns": 'RESULT_RadioButton-1',
    "First Name": 'RESULT_TextField-2',
    "Middle Name": 'RESULT_TextField-3',
    "Last Name": 'RESULT_TextField-4',
    "SSN": 'RESULT_TextField-5',
    "DOB": 'RESULT_TextField-6',
    #Select
    "SSN State": 'RESULT_RadioButton-7',
    "Phone Number": 'RESULT_TextField-8',
    "Email": 'RESULT_TextField-9',
    #Select
    "Race": 'RESULT_RadioButton-10',
    "Sex": 'RESULT_RadioButton-11',
    "Age": 'RESULT_TextField-12',
    "Address": 'RESULT_TextField-13',
    "City": 'RESULT_TextField-14',
    "State": 'RESULT_TextField-15',
    "Zip": 'RESULT_TextField-16',
    "US Citizen": 'RESULT_RadioButton-17_0',
    #Select
    "Refferal":"RESULT_RadioButton-19",
    "Refferal Name": 'RESULT_TextField-20',
    #Select
    "Position": 'RESULT_RadioButton-22',
    "Lateral": 'RESULT_RadioButton-23',
    "Lateral Department": 'RESULT_TextField-24',
    "Experience": 'RESULT_RadioButton-25',
    "Military": 'RESULT_RadioButton-26',
    "Discharge": 'RESULT_RadioButton-27',
    "Drivers License": 'RESULT_RadioButton-28',
    "Arrested": 'RESULT_RadioButton-29',
    "Parole": 'RESULT_RadioButton-31',
    "Arrested2":'RESULT_RadioButton-32',
    "Felony": 'RESULT_RadioButton-34',
    "Misdeameanor": 'RESULT_RadioButton-35',
    "Citation": 'RESULT_RadioButton-36',
    "Obstruction": 'RESULT_RadioButton-38',
    "Drug":'RESULT_RadioButton-39',
}

def random_email(name=None):
    if name is None:
        name = fake.name()

    mailGens = [lambda fn, ln, *names: fn + ln,
                lambda fn, ln, *names: fn + "." + ln,
                lambda fn, ln, *names: fn + "_" + ln,
                lambda fn, ln, *names: fn[0] + "." + ln,
                lambda fn, ln, *names: fn[0] + "_" + ln,
                lambda fn, ln, *names: fn + ln +
                str(int(1 / random.random() ** 3)),
                lambda fn, ln, *names: fn + "." + ln +
                str(int(1 / random.random() ** 3)),
                lambda fn, ln, *names: fn + "_" + ln +
                str(int(1 / random.random() ** 3)),
                lambda fn, ln, *names: fn[0] + "." +
                ln + str(int(1 / random.random() ** 3)),
                lambda fn, ln, *names: fn[0] + "_" + ln + str(int(1 / random.random() ** 3)), ]

    emailChoices = [float(line[2]) for line in EMAIL_DATA]

    return random.choices(mailGens, MAIL_GENERATION_WEIGHTS)[0](*name.split(" ")).lower() + "@" + \
        random.choices(EMAIL_DATA, emailChoices)[0][1]

def gen_fake_number():
    return "".join(["{}".format(random.randint(100, 999)), "{}".format(random.randint(100, 999)), "{}".format(random.randint(100, 999))])

def createFakeIdentity():
    age = random.randint(18, 55)
    fake_identity = {
        "first_name": fake.first_name(),
        "middle_name": fake.first_name(),
        "last_name": fake.last_name(),
        "ssn": gen_fake_number(),
        "age": age,
        "dob": fake.date_of_birth(minimum_age=age, maximum_age=age).strftime("%m/%d/%Y"),
        "in-state": random.choice([True, False]),
        # "in-state": False,
        "city": fake.city(),
        "email": '',
        "address": fake.street_address(),
        "phone_number": fake.safe_e164(region_code="US").replace("+1", ""),
    }
    fake_identity.update({"email": random_email(fake_identity.get('first_name') + " " + fake_identity.get('last_name'))})

    return fake_identity

def start_driver(url):
    options = webdriver.ChromeOptions()
    service = Service()
    options.add_argument(
        "--disable-blink-features=AutomationControlled")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument(  # Enable the WebGL Draft extension.
        '--enable-webgl-draft-extensions')
    options.add_argument('--disable-infobars')  # Disable popup
    options.add_argument('--disable-popup-blocking')  # and info bars.
    # chrome_options.add_extension("./extensions/Tampermonkey.crx")
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

def test_success(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jSignature"))
        )
        return False
    except:
        return True


def draw(action, x, y):
    print(x,y)
    action.click_and_hold().move_by_offset(x,y).release().perform()

def draw_sig(driver, coords):
    total = 30
    action = ActionChains(driver)
    sign = driver.find_element(By.CLASS_NAME, "jSignature")
    action.move_to_element(sign).move_by_offset((-sign.size.get('width')/2)+total, total-20).perform()
    element_height = sign.size.get('height')
    starting_height=total+(sign.size.get('height')/2)
    element_width = sign.size.get('width')
    starting_width=element_width+((-sign.size.get('width')/2)+total)

    print(starting_height, starting_width)

    # for x,y in coords[::10]:
    #     if x <= 1 or y <= 1:
    #         pass
    #     else:
    #         x*=.01
    #         y*=.01
    #         print(x,y)
    #         # x-=starting_width
    #         # y-=starting_height
    #         draw(action, x, y)

    x, y = generate_signature(10, (-10, 30), (-10, 10))

    # limit to 30 points
    step = random.randint(1,2)
    points = random.randint(50, 75)
    step=2
    points = 100

    x = list(np.array(x))[:points:step]
    y = list(np.array(y)*-1*.75)[:points:step]

    movements = list(zip(x,y))

    for x,y in movements:
        # print(starting_height, starting_width)
        starting_height+=y
        if starting_height >= element_height or starting_height < 0:
            y*=-1
        starting_width+=x
        if starting_width > element_width or starting_width < 0:
            x*=-1
        try:
            draw(action, x, y)
        except MoveTargetOutOfBoundsException:
            action.move_to_element(sign).perform()
    
    action.move_by_offset(10, 0).perform()

def click_element(driver, element):
    driver.execute_script('arguments[0].click()', element)

def fill_out_form(driver, identity):
    #RSVP
    click_element(driver, driver.find_element(By.ID, random.choice(all_fields.get('RSVP'))))

    #Pronouns
    Select(driver.find_element(By.ID, all_fields.get('Pronouns'))).select_by_index(random.randint(1,3))

    #First Name
    driver.find_element(By.ID, all_fields.get('First Name')).send_keys(identity.get('first_name'))

    #Middle Name
    driver.find_element(By.ID, all_fields.get('Middle Name')).send_keys(identity.get('middle_name'))

    #Last Name
    driver.find_element(By.ID, all_fields.get('Last Name')).send_keys(identity.get('last_name'))

    #SSN
    driver.find_element(By.ID, all_fields.get('SSN')).send_keys(identity.get('ssn'))

    #DOB
    driver.find_element(By.ID, all_fields.get('DOB')).send_keys(identity.get('dob'))

    #SSN State
    if identity.get('in-state'):
        state = "Georgia"
        Select(driver.find_element(By.ID, all_fields.get('SSN State'))).select_by_visible_text("Georgia")
    else:
        state = random.choice(list(us_state_to_abbrev.keys()))
        Select(driver.find_element(By.ID, all_fields.get('SSN State'))).select_by_visible_text(state)
        
    
    #Phone Number
    driver.find_element(By.ID, all_fields.get('Phone Number')).send_keys(identity.get('phone_number'))

    #Email
    driver.find_element(By.ID, all_fields.get('Email')).send_keys(identity.get('email'))

    #Race
    Select(driver.find_element(By.ID, all_fields.get('Race'))).select_by_index(random.randint(1,7))

    #Sex
    Select(driver.find_element(By.ID, all_fields.get('Sex'))).select_by_index(random.randint(1,3))

    #Age
    driver.find_element(By.ID, all_fields.get('Age')).send_keys(identity.get('age'))

    #Address
    driver.find_element(By.ID, all_fields.get('Address')).send_keys(identity.get('address'))

    #City
    driver.find_element(By.ID, all_fields.get('City')).send_keys(identity.get('city'))

    #State
    driver.find_element(By.ID, all_fields.get('State')).send_keys(us_state_to_abbrev.get(state))

    #Zip
    driver.find_element(By.ID, all_fields.get('Zip')).send_keys(fake.zipcode())

    #US Citizen
    click_element(driver, driver.find_element(By.ID, all_fields.get('US Citizen')))

    #Refferal
    Select(driver.find_element(By.ID, all_fields.get('Refferal'))).select_by_index(random.randint(1,6))

    #Refferal Name
    driver.find_element(By.ID, all_fields.get('Refferal Name')).send_keys(fake.name())

    #Position
    if identity.get('in-state'):
        Select(driver.find_element(By.ID, all_fields.get('Position'))).select_by_index(1)
    else:
        Select(driver.find_element(By.ID, all_fields.get('Position'))).select_by_index(3)

    #Lateral
    Select(driver.find_element(By.ID, all_fields.get('Lateral'))).select_by_visible_text("No")

    #Experience
    Select(driver.find_element(By.ID, all_fields.get('Experience'))).select_by_index(random.randint(1,2))

    #Military
    Select(driver.find_element(By.ID, all_fields.get('Military'))).select_by_index(random.randint(1,7))

    #Discharge
    Select(driver.find_element(By.ID, all_fields.get('Discharge'))).select_by_index(random.randint(1,7))

    #Drivers License
    Select(driver.find_element(By.ID, all_fields.get('Drivers License'))).select_by_index(random.randint(1,4))

    #Arrested
    Select(driver.find_element(By.ID, all_fields.get('Arrested'))).select_by_index(4)

    #Parole
    Select(driver.find_element(By.ID, all_fields.get('Parole'))).select_by_visible_text("No")

    #Arrested2
    Select(driver.find_element(By.ID, all_fields.get('Arrested2'))).select_by_visible_text("No")

    #Felony
    Select(driver.find_element(By.ID, all_fields.get('Felony'))).select_by_visible_text("No")

    #Misdeameanor
    Select(driver.find_element(By.ID, all_fields.get('Misdeameanor'))).select_by_visible_text("No")

    #Citation
    Select(driver.find_element(By.ID, all_fields.get('Citation'))).select_by_visible_text("No")

    #Obstruction
    Select(driver.find_element(By.ID, all_fields.get('Obstruction'))).select_by_visible_text("No")

    #Drug
    Select(driver.find_element(By.ID, all_fields.get('Drug'))).select_by_visible_text("No")

def writing_setup(lines):
    hand = Hand()

    biases = [.75 for i in lines]
    styles = [9 for i in lines]
    stroke_colors = ['black']
    stroke_widths = [1, 2, 1, 2]


    hand.write(
        filename='img/signature.svg',
        lines=lines,
        biases=biases,
        styles=styles,
        stroke_colors=stroke_colors,
        stroke_widths=stroke_widths
    )

    


def parse_svg(filename):
    svg_dom = minidom.parseString(filename)

    path_strings = [path.getAttribute('d') for path in svg_dom.getElementsByTagName('path')]

    # Extract (x, y) coordinates from the path
    coordinates_list = []

    for path_string in path_strings:
        path_data = parse_path(path_string)

    return path_string
    # for segment in path_data:
    #     if segment.start is not None:
    #         coordinates_list.append((segment.start.real, segment.start.imag))
        
    #     if segment.end is not None:
    #         coordinates_list.append((segment.end.real, segment.end.imag))


    # start = Move(to=(190+1j))
    # print(path_data[0])

    # print(coordinates_list)
    # return coordinates_list

def to_base30(value):
    base30_characters = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ_"
    base10_value = int(value)
    base30_value = ""

    while base10_value > 0:
        remainder = base10_value % 30
        base30_value = base30_characters[remainder] + base30_value
        base10_value //= 30
    
    return base30_value

    base30_encoded = "".join(to_base30(segment) for segment in path_data)
    print(base30_encoded)

def main():
    identity= createFakeIdentity()
    driver = start_driver(url)
    driver.get(url)
    test_success(driver)
    fill_out_form(driver, identity)
    writing_setup([identity.get('first_name') + " " + identity.get('middle_name')[0] + " " + identity.get('last_name')])
    coords = parse_svg(open('img/signature.svg','r').read())
    draw_sig(driver, coords)

    # Iterate through x and y coordinates, convert them to base30, and concatenate
    # base30_encoded = ""
    # segments = parse_svg(open('img/signature.svg','r').read())
    # base30_encoded = "".join(to_base30(segment) for segment in segments)
    # print(base30_encoded)


    time.sleep(10000)


main()