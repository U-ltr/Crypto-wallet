import solcx
import json

# Устанавливаем последнюю версию компилятора
solcx.install_solc("0.8.0")

# Читаем контракт
with open("contracts/SimpleStorage.sol", "r") as f:
    simple_storage = f.read()

# Компилируем
compiled_sol = solcx.compile_source(simple_storage, solc_version="0.8.0")
contract_interface = compiled_sol["<stdin>:SimpleStorage"]

# Сохраняем ABI и байткод
with open("compiled_contract.json", "w") as f:
    json.dump(
        {"abi": contract_interface["abi"], "bytecode": contract_interface["bin"]}, f
    )

print("Контракт скомпилирован и сохранен!")