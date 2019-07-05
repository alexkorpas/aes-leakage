import visa


def main():
    rm = visa.ResourceManager()
    print(rm.list_resources())
    visa.get_resource('USB0::0xF4EC::0xEE3A::NDS1MDBC1R0113::INSTR')


if __name__ == "__main__":
    main()
