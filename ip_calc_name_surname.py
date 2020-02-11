def get_ip_from_raw_address(raw_address):
    """
    Return IP-adress
    >>> get_ip_from_raw_address("91.124.230.205/30")
    '91.124.230.205'
    """
    return raw_address.split("/")[0]


def get_binary_mask_from_raw_address(raw_address):
    """
    Get binaary mask from raw adress
    >>> get_binary_mask_from_raw_address("91.124.230.205/30")
    '11111111.11111111.11111111.11111100'
    """
    one = int(raw_address.split("/")[1])
    shablon = "1" * one + "0" * (32 - one)
    bin_num = shablon[:8] + '.' + shablon[8:16] + \
    '.' + shablon[16:24] + '.' + shablon[24:32]

    return bin_num


def get_network_address_from_raw_address(raw_address):
    """
    Return networt address based on raw address
    >>> get_network_address_from_raw_address("91.124.230.205/30")
    '91.124.230.204'
    """
    ip_address = get_ip_from_raw_address(raw_address).split('.')
    bin_mask = get_binary_mask_from_raw_address(raw_address).split('.')

    for i in range(len(bin_mask)):
        bin_mask[i] = int(bin_mask[i], 2)

    for i in range(4):
        ip_address[i] = str(int(ip_address[i]) & bin_mask[i])

    return '.'.join(ip_address)


def get_broadcast_address_from_raw_address(raw_address):
    """
    Return broadcast address based on IP address
    >>> get_broadcast_address_from_raw_address("91.124.230.205/30")
    '91.124.230.207'
    """
    ip_address = get_ip_from_raw_address(raw_address).split('.')
    bin_num = get_binary_mask_from_raw_address(raw_address).split('.')

    for n in range(len(bin_num)):
        bin_num[n] = 11111111 - int(bin_num[n])
    for i in range(4):
        ip_address[i] = str(int(ip_address[i]) | int(str(bin_num[i]),2))

    return '.'.join(ip_address)


def get_first_usable_ip_address_from_raw_address(raw_address):
    """
    Return first usable IP address from raw address
    >>> get_first_usable_ip_address_from_raw_address("91.124.230.205/30")
    '91.124.230.205'
    """
    counter = get_number_of_usable_hosts_from_raw_address(raw_address)
    if counter < 1:
        return None

    network = get_network_address_from_raw_address(raw_address).split('.')
    network[-1] = str(int(network[-1]) + 1)

    return '.'.join(network)


def get_penultimate_usable_ip_address_from_raw_address(raw_address):
    """
    Return penultimate usable IP address from raw address
    >>> get_penultimate_usable_ip_address_from_raw_address("91.124.230.205/30")
    '91.124.230.205'
    """
    counter = get_number_of_usable_hosts_from_raw_address(raw_address)
    if counter < 2:
        return None

    broadcast = get_broadcast_address_from_raw_address(raw_address).split('.')
    broadcast[-1] = str(int(broadcast[-1]) - 2)

    return '.'.join(broadcast)


def get_number_of_usable_hosts_from_raw_address(raw_address):
    """
    Return number of usable host fron raw address
    >>> get_number_of_usable_hosts_from_raw_address("91.124.230.205/30")
    2
    """
    broadcast = get_broadcast_address_from_raw_address(raw_address).split('.')
    network = get_network_address_from_raw_address(raw_address).split('.')

    if int(broadcast[-1]) == int(network[-1]):
        return 0

    return int(broadcast[-1]) - int(network[-1]) - 1


def get_ip_class_from_raw_address(raw_address):
    """
    Return IP class from raw address
    >>> get_ip_class_from_raw_address("91.124.230.205/30")
    'A'
    """
    ip_class = {"A": 127, "B": 191, "C": 223}
    ip_address = get_ip_from_raw_address(raw_address).split(".")

    for key in ip_class:
        if int(ip_address[0]) <= ip_class[key]:
            return key


def check_private_ip_address_from_raw_address(raw_address):
    """
    Return True if IP address is private, and False otherwise
    >>> check_private_ip_address_from_raw_address("91.124.230.205/30")
    False
    """
    ip_address = get_ip_from_raw_address(raw_address).split(".")
    if int(ip_address[0]) == 10:
        return True

    elif (int(ip_address[0]) == 172) and (16 <=int(ip_address[1]) <= 31):
        return True

    elif (int(ip_address[0]) == 192) and (int(ip_address[1]) == 168):
        return True

    return False

def not_correct_input(raw_address):
    """
    Return True if user input is correct
    """
    try:
        ip_address = get_ip_from_raw_address(raw_address).split('.')
        mask = int(raw_address.split('/')[1])
        if mask < 0 or mask > 32:
            return True
        if len(ip_address) != 4:
            return True
        for num in ip_address:
            if (int(num) < 0) or (int(num) > 255):
                return True
        return False
    except (TypeError, ValueError):
        return True


def missing_prefix(raw_address):
    """
    Return True if prefix is missed
    """
    try:
        raw_address = raw_address.split('.')
        if len(raw_address) != 4:
            return False
        for num in raw_address:
            if (int(num) < 0) or (int(num) > 255):
                return False
        else:
            return True
    except Exception:
        return False


if __name__ == '__main__':

    address = input("Please, input your ip_address and mask: ")
    if missing_prefix(address):
        print("Missing prefix")
    elif not_correct_input(address):
        print("Error")
    else:
        print(f'IP address: {get_ip_from_raw_address(address)}')
        print(f'Network Address: {get_network_address_from_raw_address(address)}')
        print(f'Broadcast Address: {get_broadcast_address_from_raw_address(address)}')
        print(f'Binary Subnet Mask: {get_binary_mask_from_raw_address(address)}')
        print(f'First usable host IP: {get_first_usable_ip_address_from_raw_address(address)}')
        print(f'Penultimate usable host IP: {get_penultimate_usable_ip_address_from_raw_address(address)}')
        print(f'Number of usable Hosts: {get_number_of_usable_hosts_from_raw_address(address)}')
        print(f'IP class: {get_ip_class_from_raw_address(address)}')
        print(f'IP type private: {check_private_ip_address_from_raw_address(address)}')

















import doctest
doctest.testmod()
