from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
import os
from selenium.webdriver.support.ui import Select
import speech_recognition as sr
import pyttsx3
import pytesseract
from PIL import Image
import io
import base64
from fpdf import FPDF
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import log_query, update_query_status, log_response

CASE_TYPES = [
    "ARB.A.", "ARB. A. (COMM.)", "ARB.P.", "BAIL APPLN.", "CA", "CA (COMM.IPD-CR)", "C.A.(COMM.IPD-GI)",
    "C.A.(COMM.IPD-PAT)", "C.A.(COMM.IPD-PV)", "C.A.(COMM.IPD-TM)", "CAVEAT(CO.)", "CC", "CC(COMM)",
    "CCP(CO.)", "CCP(O)", "CCP(REF)", "CEAC", "CEAR", "CHAT.A.C.", "CHAT.A.REF", "CM APPL.", "CMI",
    "CM(M)", "CM(M)-IPD", "C.O.", "CO.APP.", "CO.APPL.", "CO.APPL.(C)", "CO.APPL.(M)", "CO.A(SB)",
    "C.O.(COMM.IPD-CR)", "C.O.(COMM.IPD-GI)", "C.O.(COMM.IPD-PAT)", "C.O. (COMM.IPD-TM)", "CO.EX.",
    "CONT.APP.(C)", "CONT.CAS(C)", "CONT.CAS.(CRL)", "CO.PET.", "CO.SEC.REF", "CRL.A.", "CRL.C.REF.",
    "CRL.L.P.", "CRL.M.A.", "CRL.M.(BAIL)", "CRL.M.C.", "CRL.M.(CO.)", "CRL.M.I.", "CRL.O.", "CRL.O.(CO.)",
    "CRL.REF.", "CRL.REV.P.", "CRL.REV.P.(MAT.)", "CRL.REV.P.(NDPS)", "CRL.REV.P.(NI)", "C.R.P.", "CRP-IPD",
    "C.RULE", "CS(COMM)", "CS(COMM) INFRA", "CS(OS)", "CUSAA", "CUS.A.C.", "CUS.A.R.", "CUSTOM A.",
    "DEATH SENTENCE REF.", "EDC", "EDR", "EFA(COMM)", "EFA(OS)", "EFA(OS) (COMM)", "EFA(OS)(IPD)", "EL.PET.",
    "ETR", "EX.APPL.(OS)", "EX.F.A.", "EX.P.", "EX.S.A.", "FAO", "FAO (COMM)", "FAO-IPD", "FAO(OS)",
    "FAO(OS) (COMM)", "FAO(OS)(IPD)", "GCAC", "GCAR", "GTA", "GTC", "GTR", "I.A.", "I.P.A.", "ITA", "ITC",
    "ITR", "ITSA", "LA.APP.", "LPA", "MAC.APP.", "MAT.", "MAT.APP.", "MAT.APP.(F.C.)", "MAT.CASE", "MAT.REF.",
    "MISC. APPEAL(PMLA)", "O.A.", "OA", "OCJA", "O.M.P.", "O.M.P. (COMM)", "OMP (CONT.)", "O.M.P. (E)",
    "O.M.P. (E) (COMM.)", "O.M.P.(EFA)(COMM.)", "O.M.P. (ENF.)", "OMP (ENF.) (COMM.)", "O.M.P.(I)",
    "O.M.P.(I) (COMM.)", "O.M.P. (MISC.)", "O.M.P.(MISC.)(COMM.)", "O.M.P.(T)", "O.M.P. (T) (COMM.)",
    "O.REF.", "RC.REV.", "RC.S.A.", "RERA APPEAL", "REVIEW PET.", "RFA", "RFA(COMM)", "RFA-IPD", "RFA(OS)",
    "RFA(OS)(COMM)", "RFA(OS)(IPD)", "RSA", "SCA", "SDR", "SERTA", "ST.APPL.", "ST.REF.", "SUR.T.REF.",
    "TEST.CAS.", "TR.P.(C)", "TR.P.(C.)", "TR.P.(CRL.)", "VAT APPEAL", "W.P.(C)", "W.P.(C)-IPD", "WP(C)(IPD)",
    "W.P.(CRL)", "WTA", "WTC", "WTR"
]

def solve_captcha_audio(driver):
    """Solve CAPTCHA using audio playback and speech recognition"""
    try:
        # Find and click the audio button
        audio_button = driver.find_element(By.XPATH, "//button[contains(@title, 'audio') or contains(@aria-label, 'audio')]")
        audio_button.click()
        time.sleep(2)
        
        # Find the audio element
        audio_element = driver.find_element(By.TAG_NAME, "audio")
        audio_src = audio_element.get_attribute("src")
        
        if audio_src:
            # Download and play audio
            response = requests.get(audio_src)
            audio_data = response.content
            
            # Save audio temporarily
            with open("temp_captcha.mp3", "wb") as f:
                f.write(audio_data)
            
            # Convert audio to text using speech recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile("temp_captcha.mp3") as source:
                audio = recognizer.record(source)
                captcha_text = recognizer.recognize_google(audio)
            
            # Clean up
            os.remove("temp_captcha.mp3")
            return captcha_text.strip()
    except Exception as e:
        print(f"Audio CAPTCHA solving failed: {e}")
        return None

def solve_captcha_ocr(driver):
    """Solve CAPTCHA using OCR on the image"""
    try:
        # Find CAPTCHA image
        captcha_img = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha') or contains(@alt, 'captcha')]")
        img_src = captcha_img.get_attribute("src")
        
        if img_src.startswith("data:image"):
            # Handle base64 encoded image
            img_data = base64.b64decode(img_src.split(",")[1])
        else:
            # Download image from URL
            response = requests.get(img_src)
            img_data = response.content
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(img_data))
        
        # Use OCR to extract text
        captcha_text = pytesseract.image_to_string(image, config='--psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
        
        return captcha_text.strip()
    except Exception as e:
        print(f"OCR CAPTCHA solving failed: {e}")
        return None

def solve_captcha_manual(driver):
    """Manual CAPTCHA solving with visual feedback"""
    try:
        # Find CAPTCHA input field
        captcha_input = driver.find_element(By.XPATH, "//input[contains(@name, 'captcha') or contains(@id, 'captcha')]")
        
        print("CAPTCHA detected! Please solve it manually.")
        print("The browser window will stay open for you to solve the CAPTCHA.")
        
        # Wait for manual input
        input("Press Enter after solving the CAPTCHA...")
        
        return True
    except Exception as e:
        print(f"Manual CAPTCHA solving failed: {e}")
        return False

def solve_captcha_direct(driver):
    """Solve CAPTCHA by extracting text directly from span element"""
    try:
        # Find the CAPTCHA span element
        captcha_span = driver.find_element(By.ID, "captcha-code")
        captcha_text = captcha_span.text.strip()
        
        if captcha_text:
            print(f"Extracted CAPTCHA from span: {captcha_text}")
            return captcha_text
        else:
            print("CAPTCHA span is empty")
            return None
    except Exception as e:
        print(f"Failed to extract CAPTCHA from span: {e}")
        return None

def solve_captcha(driver):
    """Main CAPTCHA solving function with multiple fallback methods"""
    print("Attempting to solve CAPTCHA...")
    
    # Try direct extraction first (most reliable for this site)
    captcha_text = solve_captcha_direct(driver)
    if captcha_text:
        return captcha_text
    
    # Try audio method
    captcha_text = solve_captcha_audio(driver)
    if captcha_text:
        print(f"Solved CAPTCHA via audio: {captcha_text}")
        return captcha_text
    
    # Try OCR method
    captcha_text = solve_captcha_ocr(driver)
    if captcha_text:
        print(f"Solved CAPTCHA via OCR: {captcha_text}")
        return captcha_text
    
    # Fallback to manual solving
    if solve_captcha_manual(driver):
        return "MANUAL_SOLVED"
    
    return None

def save_result_as_pdf(result, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Delhi High Court Case Result", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(40, 10, txt=f"S.No.: {result.get('sno', '')}", ln=True)
    pdf.cell(0, 10, txt=f"Case No.: {result.get('case_no', '')}", ln=True)
    if result.get('case_no_link'):
        pdf.cell(0, 10, txt=f"Case Link: {result.get('case_no_link', '')}", ln=True)
    pdf.cell(0, 10, txt=f"Date of Judgment/Order: {result.get('date', '')}", ln=True)
    if result.get('date_link'):
        pdf.cell(0, 10, txt=f"Date Link: {result.get('date_link', '')}", ln=True)
    pdf.multi_cell(0, 10, txt=f"Party: {result.get('party', '')}")
    pdf.cell(0, 10, txt=f"Corrigendum: {result.get('corrigendum', '')}", ln=True)
    pdf.output(filename)

def scrape_case_data(case_type, case_number, filing_year):
    # Log the query to database
    query_id = log_query(case_type, case_number, filing_year)
    
    # Set up Chrome in headless mode
    options = Options()
    options.add_argument('--headless')  # Run without opening browser window
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    
    # Execute script to remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # Navigate to Delhi High Court case status page
        driver.get('https://delhihighcourt.nic.in/app/case-number')
        time.sleep(3)  # Wait for page load
        
        print(f"Page title: {driver.title}")
        
        # Try to find form elements with different selectors
        try:
            # Try by ID first
            case_type_element = driver.find_element(By.ID, 'case_type')
            print("Found case_type by ID")
        except:
            try:
                # Try by name
                case_type_element = driver.find_element(By.NAME, 'case_type')
                print("Found case_type by NAME")
            except:
                try:
                    # Try by XPath
                    case_type_element = driver.find_element(By.XPATH, "//select[contains(@name, 'case_type') or contains(@id, 'case_type')]")
                    print("Found case_type by XPATH")
                except Exception as e:
                    print(f"Could not find case_type element: {e}")
                    # Print all select elements for debugging
                    selects = driver.find_elements(By.TAG_NAME, 'select')
                    print(f"Found {len(selects)} select elements:")
                    for i, select in enumerate(selects):
                        print(f"  {i}: id='{select.get_attribute('id')}', name='{select.get_attribute('name')}'")
                    update_query_status(query_id, "failed", f"Could not find case_type element: {e}")
                    return None
        
        # Fill case type
        select = Select(case_type_element)
        select.select_by_visible_text(case_type)
        print(f"Selected case type: {case_type}")
        
        # Find case number field
        try:
            case_number_element = driver.find_element(By.ID, 'case_number')
        except:
            try:
                case_number_element = driver.find_element(By.NAME, 'case_number')
            except:
                case_number_element = driver.find_element(By.XPATH, "//input[contains(@name, 'case_number') or contains(@id, 'case_number')]")
        
        case_number_element.send_keys(case_number)
        print(f"Entered case number: {case_number}")
        
        # Find year field
        try:
            year_element = driver.find_element(By.ID, 'filing_year')
            print("Found year by ID 'filing_year'")
        except:
            try:
                year_element = driver.find_element(By.NAME, 'filing_year')
                print("Found year by NAME 'filing_year'")
            except:
                try:
                    year_element = driver.find_element(By.ID, 'year')
                    print("Found year by ID 'year'")
                except:
                    try:
                        year_element = driver.find_element(By.NAME, 'year')
                        print("Found year by NAME 'year'")
                    except:
                        try:
                            year_element = driver.find_element(By.XPATH, "//input[contains(@name, 'year') or contains(@id, 'year')]")
                            print("Found year by XPATH")
                        except:
                            # Debug: print all input elements
                            inputs = driver.find_elements(By.TAG_NAME, 'input')
                            print(f"Found {len(inputs)} input elements:")
                            for i, inp in enumerate(inputs):
                                print(f"  {i}: id='{inp.get_attribute('id')}', name='{inp.get_attribute('name')}', type='{inp.get_attribute('type')}'")
                            error_msg = "Could not find year field"
                            update_query_status(query_id, "failed", error_msg)
                            raise Exception(error_msg)
        
        year_element.send_keys(filing_year)
        print(f"Entered year: {filing_year}")
        
        # Look for CAPTCHA and solve automatically
        captcha_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Captcha') or contains(text(), 'CAPTCHA')]")
        if captcha_elements:
            print("CAPTCHA detected! Attempting automatic solution...")
            captcha_text = solve_captcha(driver)
            
            if captcha_text and captcha_text != "MANUAL_SOLVED":
                # Find CAPTCHA input field and enter the solved text
                try:
                    captcha_input = driver.find_element(By.XPATH, "//input[contains(@name, 'captcha') or contains(@id, 'captcha')]")
                    captcha_input.clear()
                    captcha_input.send_keys(captcha_text)
                    print(f"Entered CAPTCHA: {captcha_text}")
                except Exception as e:
                    print(f"Failed to enter CAPTCHA: {e}")
            elif captcha_text == "MANUAL_SOLVED":
                print("CAPTCHA solved manually")
            else:
                print("Failed to solve CAPTCHA automatically")
                update_query_status(query_id, "failed", "Failed to solve CAPTCHA automatically")
                return None
        
        # Find submit button
        try:
            submit_button = driver.find_element(By.ID, 'submit_button')
            print("Found submit button by ID 'submit_button'")
        except:
            try:
                submit_button = driver.find_element(By.NAME, 'submit')
                print("Found submit button by NAME 'submit'")
            except:
                try:
                    submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
                    print("Found submit button by XPATH input[@type='submit']")
                except:
                    try:
                        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                        print("Found submit button by XPATH button[@type='submit']")
                    except:
                        # Debug: print all buttons and inputs
                        buttons = driver.find_elements(By.TAG_NAME, 'button')
                        inputs = driver.find_elements(By.TAG_NAME, 'input')
                        print(f"Found {len(buttons)} buttons and {len(inputs)} inputs:")
                        for i, btn in enumerate(buttons):
                            print(f"  Button {i}: id='{btn.get_attribute('id')}', name='{btn.get_attribute('name')}', type='{btn.get_attribute('type')}', text='{btn.text}'")
                        for i, inp in enumerate(inputs):
                            print(f"  Input {i}: id='{inp.get_attribute('id')}', name='{inp.get_attribute('name')}', type='{inp.get_attribute('type')}'")
                        error_msg = "Could not find submit button"
                        update_query_status(query_id, "failed", error_msg)
                        raise Exception(error_msg)
        
        # Wait for button to be clickable and scroll to it
        try:
            # Scroll to the button
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)
            
            # Wait for button to be clickable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, submit_button.get_attribute("outerHTML"))))
            
            # Try JavaScript click first
            driver.execute_script("arguments[0].click();", submit_button)
            print("Clicked submit button using JavaScript")
        except Exception as e:
            try:
                # Try regular click
                submit_button.click()
                print("Clicked submit button using regular click")
            except Exception as e:
                print(f"Failed to click submit button: {e}")
                # Try to find and click any submit button
                try:
                    all_submit_buttons = driver.find_elements(By.XPATH, "//input[@type='submit'] | //button[@type='submit']")
                    if all_submit_buttons:
                        driver.execute_script("arguments[0].click();", all_submit_buttons[0])
                        print("Clicked first available submit button using JavaScript")
                    else:
                        raise Exception("No submit buttons found")
                except Exception as e2:
                    print(f"All click methods failed: {e2}")
                    update_query_status(query_id, "failed", f"Failed to click submit button: {e2}")
                    return None
        
        time.sleep(5)  # Wait for results
        
        # Check if we got results
        print(f"Current URL: {driver.current_url}")
        print(f"Page source length: {len(driver.page_source)}")
        
        # Try to find results table
        try:
            results_table = driver.find_element(By.TAG_NAME, 'table')
            print("Found results table")
            
            # Parse table data - get all rows, not just the first one
            rows = results_table.find_elements(By.TAG_NAME, 'tr')
            results = []
            
            # Skip header row, process all data rows
            for i, row in enumerate(rows[1:], 1):  # Start from index 1 to skip header
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells) >= 5:
                    result = {}
                    # S.No.
                    result['sno'] = cells[0].text.strip()
                    # Case No. (text and link)
                    case_no_text = cells[1].text.strip()
                    case_no_link = ''
                    case_no_links = cells[1].find_elements(By.TAG_NAME, 'a')
                    if case_no_links:
                        case_no_link = case_no_links[0].get_attribute('href')
                    result['case_no'] = case_no_text
                    result['case_no_link'] = case_no_link
                    # Date of Judgment/Order (text and link)
                    date_text = cells[2].text.strip()
                    date_link = ''
                    date_links = cells[2].find_elements(By.TAG_NAME, 'a')
                    if date_links:
                        date_link = date_links[0].get_attribute('href')
                    result['date'] = date_text
                    result['date_link'] = date_link
                    # Party
                    result['party'] = cells[3].text.strip()
                    # Corrigendum
                    result['corrigendum'] = cells[4].text.strip()
                    results.append(result)
            
            print(f"Found {len(results)} results")
            
            # If we have results, save the first one as PDF and return all
            if results:
                # Save first result as PDF
                pdf_dir = os.path.join('static', 'downloads')
                os.makedirs(pdf_dir, exist_ok=True)
                pdf_filename = f"{case_type}_{case_number}_{filing_year}.pdf"
                pdf_path = os.path.join(pdf_dir, pdf_filename)
                save_result_as_pdf(results[0], pdf_path)
                results[0]['pdf'] = pdf_filename
                
                # Log successful response
                update_query_status(query_id, "success")
                log_response(query_id, results[0], driver.page_source)
                
                return {
                    'results': results,
                    'total_count': len(results),
                    'first_result': results[0]  # For backward compatibility
                }
            else:
                print("No results found in table")
                update_query_status(query_id, "failed", "No results found in table")
                return None
            
        except Exception as e:
            print(f"Could not parse results: {e}")
            # Save page source for debugging
            with open('debug_page.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("Saved page source to debug_page.html")
            update_query_status(query_id, "failed", f"Could not parse results: {e}")
            return None
            
    except Exception as e:
        print(f"Scraping error: {str(e)}")
        update_query_status(query_id, "failed", f"Scraping error: {str(e)}")
        return None
    finally:
        driver.quit()