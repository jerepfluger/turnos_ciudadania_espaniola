from service.availability_service import SpanishCitizenshipService

if __name__ == '__main__':
    spanish_citizenship_service = SpanishCitizenshipService()
    spanish_citizenship_service.check_appointment_availability()
