(() => {
  // Source + English, Portuguese, French, Russian. Operational data is excluded.
  const rows = [
    ['Guardian, motor de inteligencia antifraude','Guardian payment reconciliation','Guardian, conciliação de pagamentos','Guardian, rapprochement des paiements','Guardian, сверка платежей'],
    ['GUARDIAN: dos espadas chocan, producen chispas y revelan el yelmo','GUARDIAN: swords clash with sparks and reveal the helmet','GUARDIAN: espadas se chocam com faíscas e revelam o elmo','GUARDIAN : les épées se heurtent, produisent des étincelles et révèlent le casque','GUARDIAN: мечи сталкиваются с искрами и появляется шлем'],
    ['Formulario vencido','Form expired','Formulário expirado','Formulaire expiré','Срок действия формы истёк'],
    ['La sesión del formulario cambió. Recarga la página y vuelve a intentarlo.','The form session changed. Reload the page and try again.','A sessão do formulário mudou. Recarregue a página e tente novamente.','La session du formulaire a changé. Rechargez la page et réessayez.','Сеанс формы изменился. Обновите страницу и попробуйте снова.'],
    ['Volver al inicio','Back to home','Voltar ao início','Retour à l’accueil','На главную'],
    ['Monitor de inconsistencias','Inconsistency monitor','Monitor de inconsistências','Suivi des incohérences','Мониторинг расхождений'],
    ['Procesamiento local','Local processing','Processamento local','Traitement local','Локальная обработка'],
    ['Idioma','Language','Idioma','Langue','Язык'],
    ['Cambiar tema','Change theme','Alterar tema','Changer de thème','Сменить тему'],
    ['Guardian, inicio','Guardian, home','Guardian, início','Guardian, accueil','Guardian, главная'],
    ['GUARDIAN / CONCILIACIÓN DE PAGOS','GUARDIAN / PAYMENT RECONCILIATION','GUARDIAN / CONCILIAÇÃO DE PAGAMENTOS','GUARDIAN / RAPPROCHEMENT DES PAIEMENTS','GUARDIAN / СВЕРКА ПЛАТЕЖЕЙ'],
    ['¿Se cobró?','Was it charged?','Foi cobrado?','A-t-il été débité ?','Платёж списан?'],
    ['¿Se liquidó?','Was it settled?','Foi liquidado?','A-t-il été réglé ?','Платёж зачислен?'],
    ['Compara lo que tu negocio esperaba cobrar con el estado que informa el procesador. Encuentra pagos fallidos, pendientes, montos distintos y liquidaciones sin comprobante.','Compare expected sales with the processor report. Find failed or pending payments, amount differences, and missing settlement evidence.','Compare o valor esperado com o relatório do processador. Encontre pagamentos falhos ou pendentes, valores diferentes e liquidações sem comprovante.','Comparez les ventes attendues au rapport du prestataire. Repérez les paiements échoués ou en attente, les écarts de montant et les règlements sans justificatif.','Сравните ожидаемые продажи с отчётом платёжной системы. Находите ошибки, ожидающие платежи, расхождения сумм и отсутствие подтверждения зачисления.'],
    ['Comenzar ahora','Get started','Começar agora','Commencer','Начать'],
    ['Sin nube','No cloud','Sem nuvem','Sans cloud','Без облака'],
    ['Sin caja negra','No black box','Sem caixa-preta','Sans boîte noire','Без скрытых алгоритмов'],
    ['Datos bajo tu control','Your data stays in your control','Seus dados sob seu controle','Vos données sous votre contrôle','Ваши данные под вашим контролем'],
    ['EDICIÓN GRATUITA','FREE EDITION','EDIÇÃO GRATUITA','ÉDITION GRATUITE','БЕСПЛАТНАЯ ВЕРСИЯ'],
    ['SOLO ESTA PC','THIS COMPUTER ONLY','SOMENTE ESTE PC','CET ORDINATEUR UNIQUEMENT','ТОЛЬКО ЭТОТ КОМПЬЮТЕР'],
    ['RED EMPRESARIAL','COMPANY NETWORK','REDE EMPRESARIAL','RÉSEAU ENTREPRISE','КОРПОРАТИВНАЯ СЕТЬ'],
    ['TU RECORRIDO · 3 PASOS','YOUR WORKFLOW · 3 STEPS','SEU FLUXO · 3 ETAPAS','VOTRE PARCOURS · 3 ÉTAPES','ВАШ ПУТЬ · 3 ШАГА'],
    ['Elige qué revisar y empieza con un ejemplo.','Choose what to check and start with an example.','Escolha o que verificar e comece com um exemplo.','Choisissez quoi vérifier et commencez par un exemple.','Выберите проверку и начните с примера.'],
    ['PASO 1','STEP 1','ETAPA 1','ÉTAPE 1','ШАГ 1'],
    ['ELIGE PERFIL','CHOOSE PROFILE','ESCOLHA O PERFIL','CHOISIR UN PROFIL','ВЫБЕРИТЕ ПРОФИЛЬ'],
    ['¿Qué quieres revisar?','What would you like to check?','O que deseja verificar?','Que souhaitez-vous vérifier ?','Что проверить?'],
    ['Conciliación de transacciones','Transaction reconciliation','Conciliação de transações','Rapprochement des transactions','Сверка платежей'],
    ['Comprueba si el pago quedó aprobado, cobrado y liquidado por el importe correcto.','Check whether payments were approved, charged, and settled for the expected amount.','Confira se o pagamento foi aprovado, cobrado e liquidado pelo valor correto.','Vérifiez si le paiement a été approuvé, débité et réglé pour le bon montant.','Проверьте одобрение, списание и зачисление правильной суммы.'],
    ['Auditoría de sistemas','Systems audit','Auditoria de sistemas','Audit des systèmes','Аудит систем'],
    ['Compara valores actuales y esperados: planes, IP, seriales, estados o inventario.','Compare current and expected values: plans, IPs, serial numbers, statuses, or inventory.','Compare valores atuais e esperados: planos, IPs, números de série, status ou inventário.','Comparez les valeurs actuelles et attendues : forfaits, IP, numéros de série, statuts ou inventaire.','Сравните текущие и ожидаемые тарифы, IP, серийные номера, статусы и инвентарь.'],
    ['Calidad de cualquier CSV','Quality check for any CSV','Qualidade de qualquer CSV','Qualité de tout CSV','Проверка качества CSV'],
    ['Busca duplicados, campos vacíos, valores de error y formatos descuidados.','Find duplicates, empty fields, error values, and inconsistent formatting.','Encontre duplicatas, campos vazios, erros e formatos inconsistentes.','Repérez les doublons, champs vides, erreurs et formats incohérents.','Найдите дубликаты, пустые поля, ошибки и несогласованные форматы.'],
    ['Prueba con datos de ejemplo','Try sample data','Testar com dados de exemplo','Essayer des données exemple','Проверить на примере'],
    ['Es un archivo inventado que muestra el resultado sin usar datos de tu empresa.','Synthetic data shows the results without using your company data.','Dados fictícios mostram o resultado sem usar dados da sua empresa.','Des données fictives montrent le résultat sans utiliser celles de votre entreprise.','Вымышленные данные показывают результат без данных вашей компании.'],
    ['Ver dashboard de ejemplo →','View sample dashboard →','Ver painel de exemplo →','Voir le tableau de bord exemple →','Открыть пример отчёта →'],
    ['Descargar este ejemplo CSV','Download this CSV sample','Baixar este exemplo CSV','Télécharger cet exemple CSV','Скачать пример CSV'],
    ['Sube tu archivo','Upload your file','Envie seu arquivo','Importer votre fichier','Загрузите файл'],
    ['CSV UTF-8, máximo 10 MB. Lo revisamos en esta computadora.','UTF-8 CSV, up to 10 MB. Checked on this computer.','CSV UTF-8, até 10 MB. Analisado neste computador.','CSV UTF-8, 10 Mo maximum. Analysé sur cet ordinateur.','CSV UTF-8, до 10 МБ. Проверка на этом компьютере.'],
    ['Seleccionar archivo CSV','Choose CSV file','Selecionar arquivo CSV','Choisir un fichier CSV','Выбрать файл CSV'],
    ['Analizar mi archivo','Analyze my file','Analisar meu arquivo','Analyser mon fichier','Проверить мой файл'],
    ['¿Qué formato necesita mi CSV?','What format does my CSV need?','Qual formato meu CSV precisa?','Quel format doit avoir mon CSV ?','Какой формат CSV нужен?'],
    ['Una fila por pago. Encabezados exactos:','One row per payment. Standard headers:','Uma linha por pagamento. Cabeçalhos padrão:','Une ligne par paiement. En-têtes standards :','Одна строка на платёж. Стандартные заголовки:'],
    ['Una fila por registro del sistema. Encabezados exactos:','One row per system record. Standard headers:','Uma linha por registro do sistema. Cabeçalhos padrão:','Une ligne par enregistrement système. En-têtes standards :','Одна строка на запись системы. Стандартные заголовки:'],
    ['Un archivo genérico. Primera columna: identificador; las demás pueden tener cualquier nombre. Busca duplicados, espacios, vacíos y errores frecuentes.','Generic file: the first column is the identifier; other column names are flexible. Checks duplicates, whitespace, empty fields, and common errors.','Arquivo genérico: a primeira coluna é o identificador; as demais têm nomes flexíveis. Verifica duplicatas, espaços, campos vazios e erros comuns.','Fichier générique : la première colonne est l’identifiant ; les autres noms sont libres. Recherche doublons, espaces, champs vides et erreurs courantes.','Универсальный файл: первая колонка — идентификатор, остальные названия произвольные. Поиск дубликатов, пробелов, пустых полей и типовых ошибок.'],
    ['Bajar ejemplo genérico','Download generic sample','Baixar exemplo genérico','Télécharger l’exemple générique','Скачать универсальный пример'],
    ['Abre el ejemplo en Excel, conserva la fila de títulos, pega tus datos y guarda como CSV UTF-8.','Open the sample in Excel, keep the header row, paste your data, and save as UTF-8 CSV.','Abra o exemplo no Excel, mantenha os cabeçalhos, cole seus dados e salve como CSV UTF-8.','Ouvrez l’exemple dans Excel, gardez les en-têtes, collez vos données et enregistrez en CSV UTF-8.','Откройте пример в Excel, сохраните заголовки, вставьте данные и сохраните как CSV UTF-8.'],
    ['PERFIL ACTUAL','CURRENT PROFILE','PERFIL ATUAL','PROFIL ACTUEL','ТЕКУЩИЙ ПРОФИЛЬ'],
    ['ADAPTABLE','FLEXIBLE','ADAPTÁVEL','ADAPTABLE','ГИБКИЙ'],
    ['Selecciona el perfil que coincide con tus datos.','Choose the profile that matches your data.','Escolha o perfil adequado aos seus dados.','Choisissez le profil adapté à vos données.','Выберите профиль для ваших данных.'],
    ['Abre el CSV de ejemplo y entiende sus columnas.','Open the sample CSV and review its columns.','Abra o CSV de exemplo e revise as colunas.','Ouvrez l’exemple CSV et examinez ses colonnes.','Откройте пример CSV и изучите колонки.'],
    ['Prueba el análisis, mira las alertas y carga tu archivo.','Run the sample, review findings, then upload your file.','Teste a análise, veja os alertas e envie seu arquivo.','Testez l’analyse, examinez les alertes et importez votre fichier.','Попробуйте анализ, изучите предупреждения и загрузите файл.'],
    ['Cada alerta explica qué encontró. Alto, medio y bajo ayudan a ordenar la revisión; no son una sentencia automática.','Every finding explains what was detected. High, medium, and low help prioritize human review.','Cada alerta explica o que foi encontrado. Alto, médio e baixo ajudam a priorizar a revisão humana.','Chaque alerte explique le résultat. Les niveaux élevé, moyen et faible permettent de prioriser la vérification humaine.','Каждое предупреждение содержит объяснение. Высокий, средний и низкий уровни помогают определить порядок проверки.'],
    ['CONCILIACIÓN CON EVIDENCIA','RECONCILIATION WITH EVIDENCE','CONCILIAÇÃO COM EVIDÊNCIAS','RAPPROCHEMENT AVEC PREUVES','СВЕРКА ПО ДАННЫМ'],
    ['Compara ventas contra el procesador.','Compare sales with the processor.','Compare vendas com o processador.','Comparez les ventes au prestataire.','Сравните продажи с платёжной системой.'],
    ['Ambos reportes deben compartir la misma referencia del pago. No se cruzan pagos por parecido del nombre o del importe.','Both reports must share the same payment reference. Similar names or amounts are not used as matches.','Os relatórios precisam ter a mesma referência do pagamento. Nomes ou valores parecidos não são usados para cruzar.','Les deux rapports doivent partager la même référence. La ressemblance du nom ou du montant ne suffit pas.','Оба отчёта должны содержать общую ссылку на платёж. Сходство имени или суммы не считается совпадением.'],
    ['Descargar ejemplo de ventas','Download sales sample','Baixar exemplo de vendas','Télécharger l’exemple de ventes','Скачать пример продаж'],
    ['Descargar ejemplo del procesador','Download processor sample','Baixar exemplo do processador','Télécharger l’exemple du prestataire','Скачать пример платёжной системы'],
    ['Sube dos reportes. GUARDIAN cruza la referencia de pago y marca ventas que no aparecen en el procesador, cobros sin venta, importes distintos, moneda diferente, rechazos y referencias repetidas.','Upload two reports. GUARDIAN matches references and flags missing payments, charges without sales, amount or currency differences, declines, and duplicate references.','Envie dois relatórios. O GUARDIAN cruza referências e aponta pagamentos ausentes, cobranças sem venda, diferenças de valor ou moeda, recusas e duplicatas.','Importez deux rapports. GUARDIAN rapproche les références et signale les paiements absents, débits sans vente, écarts de montant ou de devise, refus et doublons.','Загрузите два отчёта. GUARDIAN сопоставит ссылки и отметит отсутствующие платежи, списания без продажи, расхождения сумм или валют, отказы и дубликаты.'],
    ['Archivo de ventas','Sales report','Arquivo de vendas','Rapport des ventes','Отчёт продаж'],
    ['Archivo del procesador','Processor report','Arquivo do processador','Rapport du prestataire','Отчёт платёжной системы'],
    ['1 · Reporte de ventas','1 · Sales report','1 · Relatório de vendas','1 · Rapport des ventes','1 · Отчёт продаж'],
    ['2 · Reporte del procesador','2 · Processor report','2 · Relatório do processador','2 · Rapport du prestataire','2 · Отчёт платёжной системы'],
    ['Conciliar los dos reportes →','Reconcile both reports →','Conciliar os dois relatórios →','Rapprocher les deux rapports →','Сверить два отчёта →'],
    ['SIN CÓDIGO','NO CODE','SEM CÓDIGO','SANS CODE','БЕЗ КОДА'],
    ['PERFIL DE CONCILIACIÓN','RECONCILIATION PROFILE','PERFIL DE CONCILIAÇÃO','PROFIL DE RAPPROCHEMENT','ПРОФИЛЬ СВЕРКИ'],
    ['Qué considera una inconsistencia.','What counts as a mismatch.','O que é uma divergência.','Ce qui constitue un écart.','Что считается расхождением.'],
    ['Guardian compara esperado contra real, identifica pagos rechazados que debían completarse, pendientes antiguas, referencias repetidas y pagos sin comprobante de liquidación.','GUARDIAN compares expected and actual values, declines, pending payments, duplicate references, and missing settlement evidence.','O GUARDIAN compara valores esperados e reais, recusas, pendências, referências duplicadas e liquidações sem comprovante.','GUARDIAN compare les valeurs attendues et réelles, les refus, paiements en attente, références répétées et justificatifs manquants.','GUARDIAN проверяет ожидаемые и фактические значения, отказы, ожидающие платежи, повторные ссылки и отсутствие подтверждения зачисления.'],
    ['Pago no completado','Payment not completed','Pagamento não concluído','Paiement non terminé','Платёж не завершён'],
    ['El estado esperado era pagado/liquidado y el procesador informa rechazado o fallido.','Payment was expected, but the processor reports a decline or failure.','O pagamento era esperado, mas o processador informa recusa ou falha.','Le paiement était attendu, mais le prestataire indique un refus ou un échec.','Ожидалась оплата, но платёжная система сообщает об отказе или ошибке.'],
    ['Importe diferente','Amount mismatch','Valor diferente','Écart de montant','Разница в сумме'],
    ['El importe cobrado no coincide con el importe esperado.','The charged amount differs from the expected amount.','O valor cobrado é diferente do esperado.','Le montant débité diffère du montant attendu.','Списанная сумма отличается от ожидаемой.'],
    ['Pendiente vencida','Overdue pending payment','Pendência vencida','Attente dépassée','Просроченное ожидание'],
    ['El estado sigue pendiente por más de 24 horas respecto a las fechas del mismo archivo.','Still pending beyond 24 hours based on dates in this report.','Continua pendente por mais de 24 horas com base nas datas do relatório.','Toujours en attente après 24 heures selon les dates du rapport.','Ожидание более 24 часов по датам отчёта.'],
    ['Duplicado o sin comprobante','Duplicate or missing evidence','Duplicado ou sem comprovante','Doublon ou justificatif manquant','Дубликат или нет подтверждения'],
    ['Referencia repetida o pago marcado como liquidado sin fecha de liquidación.','Duplicate reference, or marked settled without a settlement date.','Referência repetida ou pagamento liquidado sem data de liquidação.','Référence répétée ou paiement réglé sans date de règlement.','Повторная ссылка или зачисление без даты.'],
    ['Conciliaciones guardadas','Saved reconciliations','Conciliações salvas','Rapprochements enregistrés','Сохранённые сверки'],
    ['Abre un análisis anterior. Los resultados y revisiones se conservan en esta computadora.','Open a previous analysis. Results and reviews are saved on this computer.','Abra uma análise anterior. Resultados e revisões ficam salvos neste computador.','Ouvrez une analyse précédente. Résultats et vérifications restent sur cet ordinateur.','Откройте предыдущий анализ. Результаты и проверки хранятся на этом компьютере.'],
    ['Resumen de inconsistencias','Reconciliation summary','Resumo de divergências','Résumé des écarts','Сводка расхождений'],
    ['Exportar CSV','Export CSV','Exportar CSV','Exporter CSV','Экспорт CSV'],
    ['Registros revisados','Records checked','Registros verificados','Enregistrements vérifiés','Проверено записей'],
    ['Necesitan atención','Need attention','Precisam de atenção','À examiner','Требуют внимания'],
    ['Riesgo alto','High priority','Prioridade alta','Priorité élevée','Высокий приоритет'],
    ['Riesgo medio','Medium priority','Prioridade média','Priorité moyenne','Средний приоритет'],
    ['Ventas no encontradas','Unmatched records','Registros sem correspondência','Enregistrements non rapprochés','Несопоставленные записи'],
    ['Pago fallido/rechazado','Failed/declined payment','Pagamento falho/recusado','Paiement échoué/refusé','Ошибка/отказ платежа'],
    ['Casos sin revisar','Open cases','Casos abertos','Dossiers ouverts','Открытые случаи'],
    ['Prioridad','Priority','Prioridade','Priorité','Приоритет'],
    ['Referencia','Reference','Referência','Référence','Ссылка'],
    ['Comercio','Merchant','Comércio','Commerçant','Магазин'],
    ['Moneda','Currency','Moeda','Devise','Валюта'],
    ['Cobrado / esperado','Charged / expected','Cobrado / esperado','Débité / attendu','Списано / ожидалось'],
    ['Qué pasó','What happened','O que aconteceu','Ce qui s’est passé','Что произошло'],
    ['Revisión','Review','Revisão','Vérification','Проверка'],
    ['Pendiente','Pending','Pendente','En attente','Ожидает'],
    ['Confirmada','Confirmed','Confirmada','Confirmée','Подтверждено'],
    ['Resuelta','Resolved','Resolvida','Résolue','Решено'],
    ['Falso positivo','False positive','Falso positivo','Faux positif','Ложное срабатывание'],
    ['Responsable','Assignee','Responsável','Responsable','Ответственный'],
    ['Nota de seguimiento','Follow-up note','Nota de acompanhamento','Note de suivi','Заметка по проверке'],
    ['Guardar','Save','Salvar','Enregistrer','Сохранить'],
    ['Historial','History','Histórico','Historique','История'],
    ['Explicable · Local · Abierto','Explainable · Local · Open source','Explicável · Local · Código aberto','Explicable · Local · Code ouvert','Объяснимый · Локальный · Открытый код'],
    ['Alto','High','Alto','Élevé','Высокий'],
    ['Medio','Medium','Médio','Moyen','Средний'],
    ['Bajo','Low','Baixo','Faible','Низкий'],
    ['Sin alerta','No alert','Sem alerta','Sans alerte','Без предупреждений'],
    ['Cruce ventas + procesador','Sales + processor reconciliation','Conciliação vendas + processador','Rapprochement ventes + prestataire','Сверка продаж и платёжной системы'],
    ['demostración sintética','synthetic example','exemplo sintético','exemple fictif','вымышленный пример'],
    ['Sin registro','No record','Sem registro','Aucun enregistrement','Нет записи'],
    ['Sin venta','No sale','Sem venda','Aucune vente','Нет продажи'],
    ['GUARDIAN · ACCESO DE EMPRESA','GUARDIAN · COMPANY ACCESS','GUARDIAN · ACESSO EMPRESARIAL','GUARDIAN · ACCÈS ENTREPRISE','GUARDIAN · ДОСТУП КОМПАНИИ'],
    ['Ingresa la clave compartida','Enter the shared access key','Digite a chave compartilhada','Saisissez la clé partagée','Введите общий ключ доступа'],
    ['El administrador de la instalación puede darte esta clave. No la envíes fuera de la empresa.','Ask the installation administrator for this key. Keep it within your company.','Peça esta chave ao administrador. Mantenha-a dentro da empresa.','Demandez cette clé à l’administrateur. Gardez-la dans l’entreprise.','Получите ключ у администратора. Не передавайте его за пределы компании.'],
    ['Clave de acceso','Access key','Chave de acesso','Clé d’accès','Ключ доступа'],
    ['Entrar','Sign in','Entrar','Se connecter','Войти'],
    ['Clave incorrecta.','Incorrect key.','Chave incorreta.','Clé incorrecte.','Неверный ключ.'],
    ['Selecciona los dos archivos CSV.','Select both CSV files.','Selecione os dois arquivos CSV.','Sélectionnez les deux fichiers CSV.','Выберите оба файла CSV.'],
    ['Selecciona un archivo CSV.','Select a CSV file.','Selecione um arquivo CSV.','Sélectionnez un fichier CSV.','Выберите файл CSV.'],
    ['Solo se aceptan archivos .csv.','Only .csv files are accepted.','Apenas arquivos .csv são aceitos.','Seuls les fichiers .csv sont acceptés.','Допускаются только файлы .csv.'],
    ['El archivo supera el límite de 10 MB.','File exceeds the 10 MB limit.','O arquivo excede 10 MB.','Le fichier dépasse 10 Mo.','Файл превышает 10 МБ.'],
    ['El reporte no contiene registros.','The report has no records.','O relatório não contém registros.','Le rapport ne contient aucun enregistrement.','В отчёте нет записей.'],
    ['El reporte está vacío o tiene encabezados repetidos.','The report is empty or has duplicate headers.','O relatório está vazio ou tem cabeçalhos repetidos.','Le rapport est vide ou ses en-têtes sont répétés.','Отчёт пуст или содержит повторные заголовки.'],
    ['Máximo 50.000 filas por reporte; divide el período.','Maximum 50,000 rows per report; split the period.','Máximo de 50.000 linhas por relatório; divida o período.','Maximum 50 000 lignes par rapport ; divisez la période.','Максимум 50 000 строк в отчёте; разделите период.'],
    ['El procesador reporta un pago que no aparece en ventas','The processor reports a payment missing from sales','O processador informa pagamento ausente nas vendas','Le prestataire signale un paiement absent des ventes','Платёж системы отсутствует в продажах'],
    ['La venta no aparece en el reporte del procesador; verificar si se cobró','Sale missing from processor report; verify whether it was charged','Venda ausente no relatório do processador; verificar cobrança','Vente absente du rapport du prestataire ; vérifier le débit','Продажа отсутствует в отчёте платёжной системы; проверьте списание'],
    ['Moneda ausente o inválida; usa código como BOB, USD o EUR','Missing or invalid currency; use BOB, USD, or EUR','Moeda ausente ou inválida; use BOB, USD ou EUR','Devise absente ou invalide ; utilisez BOB, USD ou EUR','Валюта отсутствует или недействительна; используйте BOB, USD или EUR'],
    ['Importe negativo: revisar devolución o ajuste por separado del cobro','Negative amount: review refund or adjustment separately','Valor negativo: revise devolução ou ajuste separadamente','Montant négatif : vérifier le remboursement ou l’ajustement séparément','Отрицательная сумма: проверьте возврат или корректировку отдельно'],
    ['El procesador rechazó un pago que ventas esperaba completar','The processor declined an expected payment','O processador recusou um pagamento esperado','Le prestataire a refusé un paiement attendu','Платёжная система отклонила ожидаемый платёж'],
    ['El procesador informa pendiente; aún no confirma el cobro o liquidación','Processor reports pending; charge or settlement not confirmed','O processador informa pendente; cobrança ou liquidação não confirmada','Le prestataire indique en attente ; débit ou règlement non confirmé','Платёж ожидает обработки; списание или зачисление не подтверждено'],
    ['Pago aprobado/autorizado, pero no cobrado o liquidado según lo esperado','Authorized payment, but charge or settlement still unconfirmed','Pagamento autorizado, mas cobrança ou liquidação ainda não confirmada','Paiement autorisé, mais débit ou règlement non confirmé','Платёж одобрен, но списание или зачисление ещё не подтверждено'],
    ['Pago cobrado, pero no liquidado; comprobar el abono del procesador','Payment charged but not settled; check the processor deposit','Pagamento cobrado, mas não liquidado; confira o crédito','Paiement débité mais non réglé ; vérifier le versement','Сумма списана, но не зачислена; проверьте перевод платёжной системы'],
    ['Reembolso o contracargo: revisar la devolución y su vínculo con el cobro original','Refund or chargeback: review its link to the original charge','Reembolso ou contestação: revise o vínculo com a cobrança original','Remboursement ou contestation : vérifier le lien avec le débit initial','Возврат или оспаривание: проверьте связь с исходным списанием'],
    ['Figura liquidado pero falta la fecha de liquidación en el reporte','Marked settled but the report has no settlement date','Marcado liquidado, mas falta a data no relatório','Indiqué réglé mais la date manque dans le rapport','Указано зачисление, но в отчёте нет даты'],
    ['Referencia, importe, moneda y estado coinciden según los reportes cargados.','Reference, amount, currency, and status match the uploaded reports.','Referência, valor, moeda e status coincidem nos relatórios enviados.','Référence, montant, devise et statut correspondent dans les rapports importés.','Ссылка, сумма, валюта и статус совпадают по загруженным отчётам.'],
    ['El sistema esperaba un pago completado, pero la transacción fue rechazada o falló','Payment was expected but the transaction was declined or failed','O pagamento era esperado, mas a transação foi recusada ou falhou','Le paiement était attendu mais la transaction a été refusée ou a échoué','Ожидался платёж, но транзакция отклонена или завершилась ошибкой'],
    ['Referencia de transacción duplicada: posible doble registro o doble cobro','Duplicate reference: possible duplicate record or charge','Referência duplicada: possível registro ou cobrança em dobro','Référence répétée : enregistrement ou débit potentiellement doublé','Повторная ссылка: возможна дублирующая запись или двойное списание'],
    ['Importe esperado o cobrado no es válido','Expected or charged amount is invalid','Valor esperado ou cobrado inválido','Montant attendu ou débité invalide','Ожидаемая или списанная сумма недействительна'],
    ['Figura como pagado, pero no tiene fecha de liquidación','Marked paid, but no settlement date','Marcado pago, mas sem data de liquidação','Indiqué payé, mais sans date de règlement','Указана оплата, но нет даты зачисления'],
    ['El estado e importe coinciden; se registró liquidación.','Status and amount match; settlement recorded.','Status e valor coincidem; liquidação registrada.','Statut et montant correspondent ; règlement enregistré.','Статус и сумма совпадают; зачисление зарегистрировано.'],
    ['No se pudo validar la antigüedad del pago pendiente','Unable to validate pending payment age','Não foi possível validar o tempo de espera','Impossible de vérifier l’ancienneté du paiement en attente','Не удалось определить давность ожидающего платежа'],
    ['Identificador de registro duplicado','Duplicate record identifier','Identificador de registro duplicado','Identifiant répété','Повторный идентификатор записи'],
    ['El valor actual no coincide con el esperado','Current value does not match expected value','O valor atual difere do esperado','La valeur actuelle diffère de la valeur attendue','Текущее значение отличается от ожидаемого'],
    ['La misma entidad tiene valores actuales contradictorios','Conflicting current values for the same entity','Valores atuais conflitantes para a mesma entidade','Valeurs actuelles contradictoires pour la même entité','Противоречивые значения для одного объекта'],
    ['Fecha de actualización inválida','Invalid update date','Data de atualização inválida','Date de mise à jour invalide','Недействительная дата обновления'],
    ['Sin inconsistencias configuradas','No configured checks matched','Nenhuma inconsistência detectada','Aucun écart détecté','Настроенные проверки не выявили расхождений'],
    ['Fila completamente duplicada','Completely duplicate row','Linha totalmente duplicada','Ligne entièrement dupliquée','Полностью повторная строка'],
    ['Espacios sobrantes que pueden causar diferencias','Extra spaces may cause mismatches','Espaços extras podem causar divergências','Des espaces superflus peuvent provoquer des écarts','Лишние пробелы могут вызывать расхождения'],
    ['Calidad de datos','Data quality','Qualidade de dados','Qualité des données','Качество данных'],
    ['Completo, único y consistente','Complete, unique, and consistent','Completo, único e consistente','Complet, unique et cohérent','Полный, уникальный и согласованный'],
    ['Revisar','Review','Revisar','Vérifier','Проверить'],
    ['Correcto','Correct','Correto','Correct','Верно'],
    ['Sin entidad','No entity','Sem entidade','Sans entité','Нет объекта'],
    ['Sin categoría','No category','Sem categoria','Sans catégorie','Нет категории'],
    ['El CSV está vacío o no tiene encabezados.','CSV is empty or has no headers.','CSV vazio ou sem cabeçalhos.','CSV vide ou sans en-têtes.','CSV пуст или не содержит заголовков.'],
    ['Según reglas','Based on rules','Conforme regras','Selon les règles','По правилам'],
  ];

  const templates = [
    ['Conciliación completa: {0} referencias comparadas.','Reconciliation complete: {0} references compared.','Conciliação concluída: {0} referências comparadas.','Rapprochement terminé : {0} références comparées.','Сверка завершена: сравнено ссылок — {0}.'],
    ['Análisis terminado: {0} registros revisados.','Analysis complete: {0} records checked.','Análise concluída: {0} registros verificados.','Analyse terminée : {0} enregistrements vérifiés.','Анализ завершён: проверено записей — {0}.'],
    ['Caso {0}: revisión guardada.','Case {0}: review saved.','Caso {0}: revisão salva.','Dossier {0} : vérification enregistrée.','Случай {0}: проверка сохранена.'],
    ['{0} cambios ·{1}','{0} changes ·{1}','{0} alterações ·{1}','{0} modifications ·{1}','Изменений: {0} ·{1}'],
    ['Esperado: {0}','Expected: {0}','Esperado: {0}','Attendu : {0}','Ожидалось: {0}'],
    ['La venta repite esta referencia en {0} filas; cruce ambiguo','Sales repeat this reference in {0} rows; ambiguous match','A venda repete a referência em {0} linhas; correspondência ambígua','Référence répétée dans {0} ventes ; rapprochement ambigu','Ссылка повторяется в {0} строках продаж; сопоставление неоднозначно'],
    ['El procesador repite la referencia en {0} filas; revisar eventos y posible doble cobro','Processor repeats this reference in {0} rows; review events and possible duplicate charges','O processador repete a referência em {0} linhas; revise eventos e possível cobrança duplicada','Référence répétée dans {0} lignes du prestataire ; vérifier les événements et doubles débits','Ссылка повторяется в {0} строках системы; проверьте события и двойные списания'],
    ['Moneda distinta: venta {0}, procesador {1}; no se convierte automáticamente','Currency mismatch: sales {0}, processor {1}; no automatic conversion','Moeda diferente: venda {0}, processador {1}; sem conversão automática','Devise différente : vente {0}, prestataire {1} ; aucune conversion automatique','Валюта отличается: продажа {0}, система {1}; автоматической конвертации нет'],
    ['Importe distinto: venta {0}, cobrado {1}; diferencia {2}','Amount mismatch: sales {0}, charged {1}; difference {2}','Valor diferente: venda {0}, cobrado {1}; diferença {2}','Écart de montant : vente {0}, débit {1} ; différence {2}','Разница сумм: продажа {0}, списано {1}; разница {2}'],
    ['Importe distinto: esperado {0}, cobrado {1}','Amount mismatch: expected {0}, charged {1}','Valor diferente: esperado {0}, cobrado {1}','Écart de montant : attendu {0}, débité {1}','Разница сумм: ожидалось {0}, списано {1}'],
    ['Estado desconocido: venta {0}, procesador {1}','Unknown status: sales {0}, processor {1}','Status desconhecido: venda {0}, processador {1}','Statut inconnu : vente {0}, prestataire {1}','Неизвестный статус: продажа {0}, система {1}'],
    ['Estado distinto: esperado {0}, procesador {1}','Status mismatch: expected {0}, processor {1}','Status diferente: esperado {0}, processador {1}','Statut différent : attendu {0}, prestataire {1}','Статус отличается: ожидалось {0}, система {1}'],
    ['Importe inválido: {0}','Invalid amount: {0}','Valor inválido: {0}','Montant invalide : {0}','Недействительная сумма: {0}'],
    ['Separadores de importe ambiguos: {0}','Ambiguous amount separators: {0}','Separadores ambíguos no valor: {0}','Séparateurs de montant ambigus : {0}','Неоднозначные разделители суммы: {0}'],
    ['Importe ambiguo; usa dos decimales: {0}','Ambiguous amount; use two decimals: {0}','Valor ambíguo; use duas casas decimais: {0}','Montant ambigu ; utilisez deux décimales : {0}','Неоднозначная сумма; укажите два десятичных знака: {0}'],
    ['Fila {0}: cantidad de columnas incorrecta.','Row {0}: incorrect number of columns.','Linha {0}: número incorreto de colunas.','Ligne {0} : nombre de colonnes incorrect.','Строка {0}: неверное число колонок.'],
    ['{0}, fila {1}: referencia vacía; no se puede cruzar.','{0}, row {1}: empty reference; cannot match.','{0}, linha {1}: referência vazia; cruzamento impossível.','{0}, ligne {1} : référence vide ; rapprochement impossible.','{0}, строка {1}: пустая ссылка; сопоставление невозможно.'],
    ['{0}: no se reconocen {1}','{0}: unrecognized fields {1}','{0}: campos não reconhecidos {1}','{0} : champs non reconnus {1}','{0}: не распознаны поля {1}'],
    ['Faltan columnas: {0}','Missing columns: {0}','Colunas ausentes: {0}','Colonnes manquantes : {0}','Отсутствуют колонки: {0}'],
    ['Dos columnas representan {0}; conserva una o renómbralas para distinguirlas.','Two columns represent {0}; keep one or rename to distinguish them.','Duas colunas representam {0}; mantenha uma ou renomeie para distingui-las.','Deux colonnes représentent {0} ; gardez-en une ou renommez-les.','Две колонки обозначают {0}; оставьте одну или переименуйте их.'],
    ['Sigue pendiente después de {0} horas; comprobar liquidación con el procesador','Still pending after {0} hours; check settlement with processor','Ainda pendente após {0} horas; confira a liquidação com o processador','Toujours en attente après {0} heures ; vérifier le règlement','Ожидание более {0} часов; проверьте зачисление у платёжной системы'],
    ['Campos vacíos: {0}','Empty fields: {0}','Campos vazios: {0}','Champs vides : {0}','Пустые поля: {0}'],
    ['Estado que requiere revisión: {0}','Status requiring review: {0}','Status que exige revisão: {0}','Statut à vérifier : {0}','Статус требует проверки: {0}'],
    ['Registro sin actualizar por más de {0} días','Record not updated for more than {0} days','Registro sem atualização há mais de {0} dias','Enregistrement non actualisé depuis plus de {0} jours','Запись не обновлялась более {0} дней'],
    ['Identificador duplicado en la columna {0}','Duplicate identifier in column {0}','Identificador duplicado na coluna {0}','Identifiant répété dans la colonne {0}','Повторный идентификатор в колонке {0}'],
    ['{0} campo(s) vacío(s)','{0} empty field(s)','{0} campo(s) vazio(s)','{0} champ(s) vide(s)','Пустых полей: {0}'],
    ['Valores que indican error o dato desconocido: {0}','Values indicating error or unknown data: {0}','Valores que indicam erro ou dado desconhecido: {0}','Valeurs indiquant une erreur ou donnée inconnue : {0}','Значения ошибки или неизвестных данных: {0}'],
    ['Se encontraron {0} detalles de formato. El primero: {1}','Found {0} formatting issues. First: {1}','Foram encontrados {0} problemas de formato. Primeiro: {1}','{0} problèmes de format. Premier : {1}','Проблем формата: {0}. Первая: {1}'],
    ['No se pudo leer el CSV: {0}','Could not read CSV: {0}','Não foi possível ler o CSV: {0}','Impossible de lire le CSV : {0}','Не удалось прочитать CSV: {0}'],
  ];
  const index = {en:1, pt:2, fr:3, ru:4};
  const original = new WeakMap();
  const attributeOriginals = new WeakMap();
  const escape = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const patterns = templates.map(row => ({row, regex:new RegExp('^' + row[0].split(/\{\d+\}/).map(escape).join('([\\s\\S]*?)') + '$')}));
  function translate(source, language) {
    if (language === 'es') return source;
    const row = rows.find(row => row[0] === source);
    if (row) return row[index[language]];
    for (const pattern of patterns) {
      const match = source.match(pattern.regex);
      if (match) return pattern.row[index[language]].replace(/\{(\d+)\}/g, (_,i) => {
        const value=match[Number(i)+1];
        const nested=['Completo, único y consistente','Según reglas'];
        return nested.includes(value) || pattern.row[0].startsWith('Se encontraron ') ? translate(value,language) : value;
      });
    }
    return source;
  }
  function applyLanguage(language) {
    if (!['es','en','pt','fr','ru'].includes(language)) language='es';
    document.documentElement.lang=language;
    const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
    while(walker.nextNode()) {
      const node=walker.currentNode;
      if(node.parentElement?.closest('script,style,code,textarea,[data-no-translate],#languageSelect')) continue;
      if(!original.has(node)) original.set(node,node.nodeValue);
      const source=original.get(node);
      const clean=source.trim();
      let output=translate(clean,language);
      if (output === clean && node.parentElement?.closest('.saved-runs,.eyebrow,td details')) {
        for(const word of ['Cruce ventas + procesador','demostración sintética','Pendiente','Confirmada','Resuelta','Falso positivo']) output=output.replace(word,translate(word,language));
      }
      // Score badges contain the numeric score in the same text node.
      if(node.parentElement?.closest('.badge')) output=output.replace(/^(Alto|Medio|Bajo|Sin alerta)/,word=>translate(word,language));
      node.nodeValue=source.replace(clean,output);
    }
    document.querySelectorAll('[placeholder],[aria-label]').forEach(element=>{
      if(!attributeOriginals.has(element)) attributeOriginals.set(element,{placeholder:element.getAttribute('placeholder'),label:element.getAttribute('aria-label')});
      const attributes=attributeOriginals.get(element);
      if(attributes.placeholder) element.setAttribute('placeholder',translate(attributes.placeholder,language));
      if(attributes.label) element.setAttribute('aria-label',translate(attributes.label,language));
    });
    document.title='GUARDIAN · ' + translate('Conciliación de transacciones',language);
    document.getElementById('languageSelect').value=language;
    try {localStorage.setItem('guardian-language',language);} catch {}
    updateThemeLabel();
  }
  const themeLabels={es:['Modo oscuro','Modo claro'],en:['Dark mode','Light mode'],pt:['Modo escuro','Modo claro'],fr:['Mode sombre','Mode clair'],ru:['Тёмная тема','Светлая тема']};
  function updateThemeLabel(){
    document.querySelector('#themeToggle span').textContent=themeLabels[document.documentElement.lang][document.body.classList.contains('light-mode')?0:1];
  }
  let language='es',theme='dark';
  try {language=localStorage.getItem('guardian-language')||'es';theme=localStorage.getItem('guardian-theme')||'dark';} catch {}
  document.body.classList.toggle('light-mode',theme==='light');
  document.getElementById('themeToggle').addEventListener('click',()=>{
    document.body.classList.toggle('light-mode');
    try {localStorage.setItem('guardian-theme',document.body.classList.contains('light-mode')?'light':'dark');} catch {}
    updateThemeLabel();
  });
  document.getElementById('languageSelect').addEventListener('change',event=>applyLanguage(event.target.value));
  applyLanguage(language);
})();
