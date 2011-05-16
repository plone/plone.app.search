i18ndude rebuild-pot --pot plone.pot --create plone ../
i18ndude filter plone.pot ../../../../../plone.app.locales/plone/app/locales/locales/plone.pot > plone.pot_
mv plone.pot_ plone.pot
i18ndude sync --pot plone.pot */*/plone.po
