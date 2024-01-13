echo "installing"
winget install python -v 3.8.6
winget install Git.Git
cd C:\\
mkdir Robot && cd Robot
git clone https://github.com/felipeospina21/MagicMedios.git && cd MagicMedios
pip install -r requirements.txt
echo COTIZACIONES_PATH= > .env
echo FILE_PATH= >> .env
echo PROMO_OP_PASSWORD= >> .env


echo "finish"
pause
