-- Keep a log of any SQL queries you execute as you solve the mystery.

-- The theft took place on July 28, 2024.
-- The theft took place on Humphrey Street.

-- Your goal is to identify:
    -- Who the thief is
    -- What city the thief escaped to
    -- Who the thief’s accomplice is who helped them escape

-- FIND CRIME SCENE REPORTS THAT MATCH WHEN AND WHERE THE THEFT TOOK PLACE:
-- Result: id 295, description: theft of the CS50 duck took place at 10:15 am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time - each of their interview transcripts mentions the bakery.
SELECT * FROM crime_scene_reports WHERE year = 2024 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- SEE WHAT WE CAN FIND IN THE BAKERY SECURITY LOGS:
-- Result:
-- 1) id 256, 9:20 entrance, licence plate 6P58WS2
-- 2) id 262, 10:18 exit, licence plate 6P58WS2
SELECT * FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28;

-- SEE WHAT WE CAN FIND IN THE INTERVIEWS:
SELECT * FROM interviews WHERE year = 2024 AND month = 7 AND day = 28;

-- LOOK FOR PREVIOUS ATM TRANSACTIONS, GET THE NAMES OF THE PEOPLE WHO MADE THEM AND THEN GET WHICH FLIGHT THE SUSPECT TOOK:
-- Result: Flight id 36, origin airport id 8, destination airport id 4.
SELECT * FROM flights WHERE id IN
    (SELECT flight_id FROM passengers WHERE passport_number IN
        (SELECT passport_number FROM people WHERE id IN
            (SELECT person_id FROM bank_accounts WHERE account_number IN
                (SELECT account_number FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street'
                AND transaction_type = 'withdraw'))));

-- GET ORIGIN AND DESTINATION AIRPORTS
-- Result: Origin airport: Fiftyville Regional Airport (Fiftyville); Destination Airport: LaGuardia Airport (New York City)
SELECT * FROM airports WHERE id = 4 OR id = 8;

-- GET SUSPECTS
SELECT * FROM passengers WHERE flight_id = 36 AND passport_number IN
        (SELECT passport_number FROM people WHERE id IN
            (SELECT person_id FROM bank_accounts WHERE account_number IN
                (SELECT account_number FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street'
                AND transaction_type = 'withdraw'))));

-- SEE PHONE CALLS REGISTER AND GET SUSPECTS:
-- Results: Kenny, Taylor and Bruce --> Bruce is the one that matches more the description of the crime scene
SELECT name, license_plate FROM people WHERE phone_number IN
    (SELECT caller FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60 AND caller IN
        (SELECT phone_number FROM people WHERE passport_number IN
            (SELECT passport_number FROM passengers WHERE flight_id = 36 AND passport_number IN
                (SELECT passport_number FROM people WHERE id IN
                    (SELECT person_id FROM bank_accounts WHERE account_number IN
                        (SELECT account_number FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street'
                        AND transaction_type = 'withdraw'))))));

-- GET ACCOMPLICE:
-- Result: The accomplice is Robin
SELECT name FROM people WHERE phone_number =
    (SELECT receiver FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60 AND caller = '(826) 555-1652');
