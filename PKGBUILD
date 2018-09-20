# Maintainer: Adam Wendelin <adwe at live dot se>

pkgname=texttv
pkgver=0.1
pkgrel=1
pkgdesc="SVT Text-TV browser in the terminal."
url="https://github.com/Crablicious/texttv"
arch=('any')
license=('GPL3')
conflicts=('texttv')
provides=('texttv')
depends=('python' 'python-setuptools')
makedepends=('git')
source=("git+https://github.com/Crablicious/texttv.git")
md5sums=('SKIP')


package() {
  cd texttv
  python setup.py install --root="$pkgdir/" --optimize=1
  # doc
  install -d "$pkgdir"/usr/share/doc/$pkgname
  install -m644 README.md "$pkgdir"/usr/share/doc/$pkgname
  # license
  install -Dm644 LICENSE "$pkgdir"/usr/share/licenses/$pkgname/LICENSE
}
