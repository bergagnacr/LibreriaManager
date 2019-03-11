#include "comprasproperties.h"
#include "compraspropertiesplugin.h"

#include <QtPlugin>

ComprasPropertiesPlugin::ComprasPropertiesPlugin(QObject *parent)
    : QObject(parent)
{
    m_initialized = false;
}

void ComprasPropertiesPlugin::initialize(QDesignerFormEditorInterface * /* core */)
{
    if (m_initialized)
        return;

    // Add extension registrations, etc. here

    m_initialized = true;
}

bool ComprasPropertiesPlugin::isInitialized() const
{
    return m_initialized;
}

QWidget *ComprasPropertiesPlugin::createWidget(QWidget *parent)
{
    return new ComprasProperties(parent);
}

QString ComprasPropertiesPlugin::name() const
{
    return QLatin1String("ComprasProperties");
}

QString ComprasPropertiesPlugin::group() const
{
    return QLatin1String("");
}

QIcon ComprasPropertiesPlugin::icon() const
{
    return QIcon();
}

QString ComprasPropertiesPlugin::toolTip() const
{
    return QLatin1String("");
}

QString ComprasPropertiesPlugin::whatsThis() const
{
    return QLatin1String("");
}

bool ComprasPropertiesPlugin::isContainer() const
{
    return false;
}

QString ComprasPropertiesPlugin::domXml() const
{
    return QLatin1String("<widget class=\"ComprasProperties\" name=\"comprasProperties\">\n</widget>\n");
}

QString ComprasPropertiesPlugin::includeFile() const
{
    return QLatin1String("comprasproperties.h");
}
#if QT_VERSION < 0x050000
Q_EXPORT_PLUGIN2(compraspropertiesplugin, ComprasPropertiesPlugin)
#endif // QT_VERSION < 0x050000
