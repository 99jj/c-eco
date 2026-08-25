from __future__ import annotations

import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_ATTRS = {"href", "src", "poster", "action"}
IGNORED_PREFIXES = ("#", "mailto:", "tel:", "javascript:", "data:", "blob:")
REMOVED_PATHS = (
    "api/review.js",
    "assets/index-C_KiMpFd.js",
    "manifest.json",
    "offline.html",
    "docs/migrate.sh",
)
SUSPENDED_PATHS = (
    "tdr/tdr-mathematics.html",
    "tfp/protocol.html",
)
HASH_SIGNATURES_GLOBAL = [(2, '29cea29f533f6b10329472e10d429228de776b564f700a44c24de8d2d76a84b6'), (2, 'acb13bc6cd501ab9eca2b45de05d34484372492eaa18f8285c812557aa2e95e4'), (2, 'df135c0b5e1d20bf2abb4e01d97152adca412a861d152430d40cbd0a2b7dc535'), (3, '2ed8ce477af29729e3a9f5c32b8cfb0266ac815385af117d4cd4614e90be6592'), (4, '78a8ed0ca07ae113b9c9547d14a49714e3cda4f603cd331f77d4c4e668656ccf'), (5, '26e92e8d3b3093b5838fe7c57057e9ff0a0c6a7a51c5ef2b3e1877d9431e8fc8'), (7, '237fc9571e20805943bb8c754d2f13bea1d2f4858f83d3205cdc22f38e1d0d09')]
HASH_SIGNATURES_BY_PATH = {'de/c-eco.org.html': [(2, '7f2471cec06360055c35c0a4f6aa0d8ce50d8af236a550e1386245dc6ca60a28'), (2, '87c3bf636f4b4c196bc8278e6fda1cbe8830a541a9a17e642998666eb4ce4054'), (3, '00f8453afd067a54aeaf16725fef7ad6c036b19be00894be33028bbec6dcfff7'), (3, '7805f15a3eb4a40d9a2046078bf36d71130fbd8a1935b248419e1b3f9a866ea7'), (3, '943a9774c31f57ebb4b856f3e6273a8cb0dd7c006caf34d93f7447d59e54a47d'), (3, 'df4a5d2954ece177392406e956afdc13271cbee98ab6cdb8e212cdc0c8c85d78'), (3, 'e8386487233b888bb8f6ed21d7a36486a1642dc971a1a79577415c3ae9a52e3c'), (4, '02b3e746aa8b8f9dae8dd1cb13bbfc894eedc9edaf20a2291c4094b9f200c633'), (5, 'c7801d4dfec5c0b552510b6268dbd2ba00fddfa3351a1689a6e273a55bb2b7ec')], 'fellowship/cases/fellowship-cs-brumadinho.html': [(2, '84495362da680d61b9f0f6685b17fa903b8c8c3efb76fefc05d44e0a0ef7239c'), (2, 'cf772aa46cd227528708c014fd2150f06921b788d587b55f1b9157e711487d97'), (3, '0b5c94047416e509577a28715265a13cd7f7b4a5ac0410f3e0bafd3ab78458df'), (3, '3f33ea0b92dd43ee42312a48e3e51be23234590c084f1df2740bee3e23a42705'), (3, '405cc972291ebe1b11dfd4acc8653ce3bac8c12ca46324cf1b645c1229b4b626'), (3, 'ade814637bb74cf853501222891c07e4b7efa4357bbc33fff122f60613ccab1a'), (3, 'c4b76872420e523bdc8bd384a548f8f1ca4150abed1c5b128633de5f5cb1ed9e'), (3, 'cfb4bfdaf3021ae97733339ee85a760303b4c673b874708d8772c96be3e93bfd'), (3, 'd8dd87c26791f90243f0d5f29cfe8741999840de3d20a9ea59e5ed31a3e6e991'), (3, 'e91ead1ee5809e1fe60e8291da1e519d8f924f55499cfa953e0fd241c9330ea1'), (3, 'fb88c2542e7e85de311f746393318898dad88895b12c0354682191b16a54e67f'), (4, 'd621dc2056b01eace76e91204b6b90547e7d35129d38a20efe529ebfb890d353'), (9, '84aee6461e8065a5defb5d2a5cc3b963f336671fcaf294005105644766f12f5a')], 'fellowship/cases/fellowship-cs-yemen.html': [(2, 'e8771cf2e3407f91881badb6f33aefdf58a6b711f76211a90761d1edafd7206a'), (3, '5e0bc68cb27ff9a76ec3470159a537be52f64530791cad9372ffc813d4a43160'), (3, 'eeeab679092422a14397c49f4bbdc4acb1cb01da8209c5a5e49693d199e87874'), (4, '135c7455673ac71b02d3bc5c803cb34f73412da122a9a410621ac17e52a301c3'), (4, '85bc905feecdd0b5920ed4e1aeada57c19c0f68c9d78f050507ebad70e4c2fc4'), (4, 'cceac9d93cb89e3c036776062799beb974f528d5a4a61c46350a1e83393ef84b')], 'enterprise/alpha.html': [(2, '1a05ea25ce89fca3a780864f80a6d53b94ece4c98698534720ff405d3cbfd351'), (2, '262587bcef209d1b448ef305dc714f16936f0c1cddfba9226ed76b6120423f69'), (2, 'f39e895c2aa3955c9944186cb4aaa366f0a6024cf8404d1a9cbdd90fd8540c32'), (3, '5d8d924ab03f5928b5ea66ddd21dbbcb71019b2fb1a7c7b5f4949079efaa9689'), (3, '714963c92d8fc950d099465aa668ae17d3d7b9d8dbd24f3433f9c8b36c413897'), (3, '93d7c8fe48bf8c750579067e873112ced3136a4c46558918a3a268ecaf751895'), (3, 'ed02543c68f2b9395229cd1601f03dd2217d5a6750c53eb1608aeaf63196e257'), (4, 'cd7c1d00fc8aedfcb63ec2c44e82ca2fe9153b1e763c1614917db6b424235267'), (4, 'd01c0fb81e3b20e9493e3201190d98d6ef0df2b5e8a37f5672e6d0ef2835554e')], 'amazon-lab/amazon-lab.html': [(2, '31c5ce3b43debbc0ab3c375c38736d15a589c2a19957941331c02f78dce7f057'), (2, '442ec7333914c1be943916efc4aefe89dc33a5488e0d620ab3fc488b1069e23f'), (2, '52ebffac17c2119bc93f7fec827dbcfb2b6f67184eff61431d067324c23231f0'), (2, 'c3ce7a75c22ab2cf0aa924dd7e39b2d59b9377fcba7ac4da8f1f171d318941ea'), (3, '26259b8fefe9e8efe3a79012a3bafe6dc6cf30cbcf09b36610ce4d03bbc8fab8'), (3, '4d25ec017c6548d4b23dab7e9ab7980470407716fd87f88e06c8d44764722fa7'), (3, '68861ef9e29ecff987e951224e03971bdc2753e86a179e0d5a084e48c7236a09'), (3, '75adf4a504c3dfea76086673c9e879d67b323f5431cf8ca4249c53e3d2216198'), (3, 'ddac847cc2a176804ac0fbfe75a64c119797c151e562a9d390105d625b238c99'), (4, '2c54fdc1aa5cb24f1e0c0facebfcd2cda83840449e38a323210de36618da2606'), (4, 'b8aaa4686cb2bc0fd48f69d07334fd051e2eb4e4f9c0ab6750052f3aa27ecabf'), (5, '449a40eb9cccb2a61559849e49cf90d1d71ecbc70343ee149d101e67b26529d2')], 'fellowship/cases/fellowship-ec-tapajos.html': [(2, '6bab7f6b58895ca1dc5e887fb6da0be769a70e8995c58ce2c7ddab2bcb3510cd'), (3, '83f104ae9fac8612170f7c26eae98c1c666f204a335b4972af87677c87a787ef'), (5, '08f758f6805e6db8e949c3e6aeb2437d3a8a55fe141b7a849edf70edf4406ae4'), (5, '21ade5e75ad114b9592640e9f4a37282ec01a24bdfdb58c38c1a48c24ec26ae9'), (7, 'fddb4be11d16c69bd1518ba9e604562e91d35aa5bfca2e9abff9415f19a01aab')], 'tdr/tdr-hasse-foundation.html': [(2, '66dfd03ff99f2cda43409b9278f62fb0871f5dee85c6620d51f230c050da56ab'), (3, '09d3cc643970284b1ebaac9be9c21adac81ed78c58f5111965b19813e47be61c'), (3, '3e57ff7752ca029488509f11b0b427dbe4949463e550c51cdce6c19449984ca8'), (3, '6c8b2f055539e187b5c9d66bba1efe59328b542295abaaaabb69c32c38e1d1d9'), (3, '7bf34aa733c8bdf49a9292246b06ff60d78167776491dab654ef3993684a5da6'), (3, 'a0eb219c3701689768f790f05cc793475d7886947480825156d952d8c4b5e842'), (3, 'c753bb8cf800d910e69ceef778b874e2647c2fd52df188cfb35d1b7096f4bd54'), (3, 'fce847bf624513bf51ac55918de45a9d6cda4b86c9a39c7413300eeb0c839c4c'), (4, '541316d7101d658811e92fc0d13ce50b31f132800d011524bfff3491c66ae983'), (4, '90436105efc157a839f46c99292fe2f1f392674e219e46c77ebf0da88f260bbb'), (4, 'd3f1f1523ba5309c2a325c15d1f5b8244d95e113c707fcbb5fcd2330fdc84713'), (4, 'd671e9255368a869c538851263f8e496b64712fc3ea0162e0e1bdf9dabe8d003')], 'enterprise/pilot.html': [(2, '6623493096d0535399c1a6f265cb25416c21b4bced0121a2ff27703d9503b6a3'), (2, '9c1636e18e6e28e80f3797bdb6b7d51796cce0545c6b30f089fd019751d18b67'), (2, 'cab11d7afc08adf8c12b86dee957a4e40640c38546ee0171c0e60d725a4dc7eb'), (3, '31c1c7e0ffb7e86af7888ad8437e01556c881790b0820cad8d31138cf2806ebf'), (3, '5c0c536fd7489c8e1e4335faec238f1bfe52217ae7dcad101d8aacf3b36387da'), (3, '8bfea7954657566efa3de3bcd018311e3f663de9535f5bce7bbf37ccc88fddd5'), (3, 'a8c43883275a2e71cb4c12a1b9cf5c3d42bc68d986f538dfbac8970dc5f78991'), (3, 'c4a638e6ec2018d814422b7b2a405945d7f00f45c217814fb96738a75b852e6b'), (3, 'd7c1a174fe5a6f172f076711fae5c1f3066a6b4e0ca1c8976ff245ee9184027b'), (3, 'ed9ece9f7e58684279ef7f1efd911713ee508b3f91506bcacc8a5ab26403e20f'), (4, '20fb6498da7dd0a260cd1684491d7d29d839e24f75e3d4a536d14120e747d10c'), (4, '2369dfe3b696bae22e28625f1f1079b22b8564b6205488dcdc70d7957100dd3d')], 'enterprise/executive-summary.html': [(2, 'bc12b9dd0608273a0346c68fcef77dbf5aa0ddeef452753f7dde0e6421aea981'), (3, '1b0cefaf4bad28a0045620e8a584de457ed76b6a9ccd638579bc7529124329a8'), (3, '1b0f7615767ba25cc6bfeb28ac5ab31a51480705aadf069df69a75d8f184f008'), (3, 'c749e0ea9260b393b1f79c12679d0fe62716e94063f0e1e1dda31cef579d05ec'), (4, '24d7a0c2719542a146c6c94aee7d5e90e2b3cfb562340c58aa2c1ce6fbac23d3'), (4, '289cd51bd087609ed73b11e9bb7e5d30d18c3fd2d892ff29119c9bfd8f0aecd5'), (5, '9dfb60029591967bbb69368bfe64f41e33c94fc73f9736e859245f1b5e52e935')], 'content/community.html': [(2, '2546f14af61dfe9b6ed45eee2f424ac75fc561a9182dc304e1f8467aa7a74fb3'), (3, '39ba966371909aad06c6b5ed67f23459f65611ad28102e91a21b830e6fc72ea5'), (3, '7355bcd945c587f0c1f02e1935274417a158d1fbe7f5137bee75a4d4b17f1f28'), (3, '8ed77203daa8d2f7890bc2de83eb10ee91fda57dca5c65bd9b5f8af8ff3fa899'), (3, 'c47c667e2268e8736a44404d2dcaca00b54a636d4469f61986316835431bcaa3')], 'pt/community-pt.html': [(3, '81d3d8547bf39f2f6ec752f76e807474a9bae05220eff7514641e9b1727d959f'), (3, 'ae4213e1a9556b25ebe73955d768cd2b94b420f6be58154aa0ee8e7712a7f5c6'), (3, 'e4fc01b8e583e12c536d6bb6b62e74e8332b8665aca89bc9989ec1afa2a4ed9f'), (4, '28064134aab0a16ebf3aa7ec2c17a8b20f44a4daa8ed9ef2950a15b6fa9ecbce'), (4, 'e84cb15e587c113acdb4f6c96e55a448bbdfae1de0b1de3f1fe770c02498e351')], 'english.html': [(3, '45aae4ab04dcc5cc6672fb81b214b0ce7ec4b0738005397079470ddb6e16df9d'), (4, '8bc4dded9760701f463ce3c53ce8a83dd9bd29d5420531a1a69e0f236abf4058'), (4, 'f132fb92f92e09c100b0eb67c1565b8e73afff870342471a37449dceb240f078'), (5, '7184185abe7815e0833e763479b00b18e2e2267a20d0161c4630fbb5a69102a0'), (6, 'aa4baaf46641db162bf40f72b38d6d846bf04391468c3966c0fc141dfc822012'), (6, 'd7991d920fdddadd8a9aaf80033d5d86581485f2288eb111706a50aa8f7953d8'), (7, 'e0a1df6ca1500e19261cc9fc5236b7e61b1c255009f8852bf85102c3e3dbfdf6')], 'fellowship/fellowship.html': [(2, '9acdb813cd9c699221ded1a44952dd24a3291ab602b957d37ac6ef602e5e250e'), (3, 'c7157b624e1564beef28a329638a2e2f629e3c0ae133f5d78f7d8c9dca333a3e'), (4, '0d6cc959f16971b447cbab5e7acc349a1f929b5f78287d4381d75f38bea2d11d'), (6, '67642db9adcc7f36a4e6a405ea67957b000896db84711bb3cf8cfcbfae82870e')], 'fellowship/fellowship-portal.html': [(2, '9acdb813cd9c699221ded1a44952dd24a3291ab602b957d37ac6ef602e5e250e'), (3, 'c7157b624e1564beef28a329638a2e2f629e3c0ae133f5d78f7d8c9dca333a3e'), (4, '0d6cc959f16971b447cbab5e7acc349a1f929b5f78287d4381d75f38bea2d11d'), (6, '67642db9adcc7f36a4e6a405ea67957b000896db84711bb3cf8cfcbfae82870e')], 'foundation/memo.html': [(4, '0e5a563e1a6af48845338627e810c5d6c495a4f380c874538c860406197f8359'), (4, '29f7f32c585d79924985ee534f2d2c71fd006d41bb2837f466626ad1830d4aaa'), (5, 'ce7c99f52ea2951d8bf6396902897b52a52de2c0b365f4a36d11b2f9ea6d01e1'), (5, 'e3a7c3212f81b8ecb19e58a23c938f13c5d11e3847bee91bbfcdd7e7a0ef3389'), (9, '84aee6461e8065a5defb5d2a5cc3b963f336671fcaf294005105644766f12f5a')], 'pt/piloto.html': [(2, '3e5846fc73ed3a5527fb941bd064545acba45a006c7e2ee22579fb18178d1b6f'), (2, 'd46983a0e909fe1afb395d36a98070bf35180d8e8c45ff3ab8838ba653f3d70b'), (4, '715e6e6ff70e6237f14d5187dec75a80519dbfac109566ce3ed930af1ae1fa17'), (5, '330f1750cfbb2e18d4af5fd312e2bd2aee3be252e6bbb1fda2308cd1776bdd4a')], 'foundation/ism.html': [(2, '30f6936695bb0b36985545943534bbc41676aecbae46c042a386960da6a7a50d'), (2, '5351f81dc4afd5f84baeaeb2217db4f9bab705f22351571adb21bdd575d33175'), (2, 'c0c7f1bd4f90aa467c4341254dd1948f3de44c56b3dbbfe25e6f6243f48fb61c'), (3, '1a1c780489ef1da7c3846152894683d15917b6f0b0d7736adfa2f1e812f17268'), (3, '34600f690681381961630cca55014d9d4685be72182ee3e42be1e81557bcf7b9'), (3, 'b91cc03b07ae44d964d688f7eea06904e5fe0fdfe517cf1a5903574247d671a8'), (4, 'ff363e77d8698add44800513e9acae3e0ea92c158843a068c394fdf3af657348'), (5, '00b5736341970fbfa8a9e36ea91852768cadb83cfc00f98b4a902b0166a92f1e'), (5, 'd38550e12bdd6176f772f919fb80f975490f5b2951108cb14f6c748234fef609')], 'sectors/living-labs.html': [(2, '26f012cb8e4262534cd7a466e84f5fcb735d5897b4dc706d7a8fb773a6e19c31'), (2, '6606ae313989928c5e792befa9c84c4a7fed287390d96446d6a98e1386be7037'), (2, 'e1dc9d44bdf96c10c275d0cf7d1ed9f5db403819b1c3b8ad0e05f1d41a489879'), (2, 'f3e15f5727933922f84eb1de7afc216d48231938dee88e779cf0536ca9d09f29'), (3, '64989ccbf3efa9c84e2afe7cee9bc5828bf0fcb91e44f8c1e591638a2c2e90e3'), (3, 'bc16f7e5d0f05b3edf767855a6c096d92418fa703cef052853e4496240c56b46')], 'sectors/emergency-sectors.html': [(2, '2574b1dca563b003d85bbbe8d40b44dab5fc808e4267aa239bc6fe7ade3a6702'), (2, '5e6cbad511cf0eed4f60f60ca070d9e4da980fdabee96e8dd4cd5b80375ab803'), (2, 'efaa3d61338e771bbbebcf7e85d91cd26d6b4a3fbe29e04a5f1f5d8609edb8ea'), (3, '1f5d19fd1d3ecc061d066814e80a1b232a8328bed787059de3c027e142a0f9f7'), (3, '21f5553beb1129009215447c64f4622e02a3559978998a5d1c2305c23a7f8127'), (3, '725c102b0963fb762b5568f79e05ebe2b4931c9f9f4e3859389362001b96cda2'), (4, '3af385a6e6c10060e37ff5206434271ae6432aecd656fa640690dd96cfc8c773')], 'doctrine/esl.html': [(3, '6d9d5dee292b4cbb282cb7588a264f3c91de00c4dcbdf3f8a0728df737b13b87'), (3, 'ade814637bb74cf853501222891c07e4b7efa4357bbc33fff122f60613ccab1a'), (3, 'd6c0e84773054df9f40d8da299e309e897c3a0ecc305be0228eee11d90eb8cfa'), (4, '5a0d97dc04d0cb29cdd5a870d9bd6d0275e011b33d61a816407d142283bb509f')], 'doctrine/unidroit.html': [(3, 'ade814637bb74cf853501222891c07e4b7efa4357bbc33fff122f60613ccab1a'), (4, '5a0d97dc04d0cb29cdd5a870d9bd6d0275e011b33d61a816407d142283bb509f'), (5, '1c9d5934c07dfbaad870dc3c47aef6da5112e17720f091cb4b53a190267977de'), (6, '9e7fa9265422428c48e7d4bbb734f64f2ba6969eff055f897780511eb861b476')], 'foundation/partnerships-interest.html': [(3, 'b057348664e9fc52dfc7643e634efb63616b0ec324488069d64ab858d87d2b6e'), (4, 'fef97cc22f246b0b5da854c5e402e23d3a3aec636191d7a5eaf166c7bf53fb47'), (8, '8a1a7e693a3421d5c80121724bc2372fc80468d4e12da6ddd86c63ab2e9896c0')], 'foundation/partnerships.html': [(3, 'b057348664e9fc52dfc7643e634efb63616b0ec324488069d64ab858d87d2b6e'), (4, 'fef97cc22f246b0b5da854c5e402e23d3a3aec636191d7a5eaf166c7bf53fb47'), (8, '8a1a7e693a3421d5c80121724bc2372fc80468d4e12da6ddd86c63ab2e9896c0')], 'foundation/institutional.html': [(3, '45aae4ab04dcc5cc6672fb81b214b0ce7ec4b0738005397079470ddb6e16df9d'), (3, '710092e7ffdb6b3b140804fcfdc45d3276ea3145aec50a3ffef5177f0181574a')], 'fellowship/fellowship-amazon-lab.html': [(3, '0344f784c6f8cf48f0cf6aa53c53206efad44f7b0c9ad51f06e85d0cef13f9d7'), (4, '95d57ab921ac0963e7a3b7acd802be18010458b7aeb84c8fffd0a6a5f17f98e4')], 'fellowship/fellowship-spn.html': [(4, '5841f546438ae2c9e8ffd69b0d12a2041a3610c66c9457ec2e11549fd695b214')], 'enterprise/enterprise-folder.html': [(2, '09dd80803610c2f23d6092f71d2a5ad7d41cd193223eef2487975cd840b8abe0'), (2, 'e8f93e7cf21efab1da3dd8383185c206bfe438e9d4b555d819883e874e80fe53'), (4, '2369dfe3b696bae22e28625f1f1079b22b8564b6205488dcdc70d7957100dd3d')], 'enterprise/pathway.html': [(2, 'e8f93e7cf21efab1da3dd8383185c206bfe438e9d4b555d819883e874e80fe53'), (5, '5d02d9725dbf2d0ef8b3611670176c391bb8919e19f80f1ce344abb316ecc6b5'), (7, '5d92af1b045aa3e455974de2f064d5b1ee71afd06e8ed5fc3fff264f153685f4')], 'pt/pt.html': [(2, '03426c90e5a4fcf76d3c688c2cedcf2a5c3e200f14e5de0792c3c8d8762f68a5'), (2, '99eef453bbbe5645a48a3ab5593269b378f8b1c002e67e0d34b21b11d8025e41'), (2, 'a7e0e29123e0a0de59fa75a1cf0f3f0f1e1ade498b97eccbb0aef5f86311b4f0'), (3, '1a348dfc8ec9f28a5ac6cb4a9245ee8794c210e1dfe6484f22d66766d1ede1bb'), (3, '863917b08b6cc457371f65c4b98432c65826d84b4476915359a04271ddedf2cf'), (3, 'ade814637bb74cf853501222891c07e4b7efa4357bbc33fff122f60613ccab1a'), (3, 'bc16f7e5d0f05b3edf767855a6c096d92418fa703cef052853e4496240c56b46')], 'doctrine/screening.html': [(4, '38a59ab8b83858bef7a0116d3a06595fa33493d5aebe8b1c55f54090685791f8'), (4, 'ab5947ed509d858522520b2fb0c749a8a1b59a2865e55898a45f18731d3c2b70'), (4, 'd0479db54dfe98f43ca886771e1a96e6df2115e928ce6d3d2fbffddf3ba75298')], 'enterprise/portal.html': [(3, '9911700d4dcea947745925b4839953d8ba2c91ce595223bbfa0f4a8b969ade5e'), (4, '2ebf9742f7d19b00d54e3373048f9e40e8952af03eb81d20b51151091e20bf01'), (4, '49353e3d157d685f28ead4dd306b14477c637f57164e3a1062a0c724db3fe21c'), (4, '6c224874b8428049818c0b711f0dacad2789604207b31607ee522afbe46d3c26'), (4, 'a1fd7af7204722d25b9d61f4964d932b37560e6333993e1f2c5bc7ce5003f9fd'), (4, 'ae98cf212f16245504a27f367e9c722633c23c954a781d6a2806f3d64a564600'), (4, 'b4da761c7db1775415b4f2938dbd935828d27098fe0aa727ed322938aa6c2838')], 'enterprise/enterprise.html': [(3, '37f3752bd96c2ad350b9552af79dd3b4af6f408780255f3a3eabdbb584532993'), (3, 'ef70738da41c07a3bdc58a7878757117bd36872fa2623d445c5de70bc91cb390'), (4, '62c726062774c311da84eec6211e2d68ccc8d7c6b396a18b237f87390b51bf09'), (4, 'a4ba15fc9141fba6bbd605948477c9ff632fdd8857b0103fbd86e81e737035bb')], 'foundation/about.html': [(2, '4d850ec0e875c37c699b613ea93877d86171f0e93630f9c8ae9783a1a7d302ce'), (3, '93b6853b28cc264e07a16096ad1648f5390259a9f3aa250d2703445b45335444'), (3, 'd83fc22753e235c5f978c0aa1932e274f7af0822abae5c008e87bbab4e47ee2f'), (4, '71b76a33b2ae36f33ceaa8f68797d21f09bb64022b9ce047913540c0c6307ab8'), (6, 'a489715a7994cd0e22cb8010d6250c928c46c133300f817c28c707f5547880ef')], 'foundation/foundation-governance.html': [(2, '4311509a3fb2811dffb44ecde525bad6a68d031fe451f4c393ec3b99d844f857'), (2, '49466df542153a047f4871ca2529c203225568e5e3d41d546e2681da97ab49e7'), (2, '4dfd68e2c8b13d4f146a12c4d378a4011a4e618401ebb9e467e675d735220d93'), (2, 'a8bf82b72d4f92186bdea541dcf87f103dabbeaf6fb2c3c15ab25ee79739c129'), (2, 'fd197af1b38f20f9e3899a49aef1e74bbbdeb8202092a8ca66eab5478b56d52a')], 'fellowship/cases/fellowship-cs-tapajos.html': [(2, '068e5c97479246ea9e56c1a19c8040e25025d73813af69f2f66fd4cc4ac9ca83'), (2, '520ad13721991b2e453fad3a631ab1adbf27d4d96b390ee6b24944322c3808d2'), (2, '77d9ef8e3c4dbba65759689228cfcea0820c3a8bcc8473770c4c9953d5d154ea'), (2, 'a667f63e75ca26e57d3b420a542a354722d5ea954c6a8821e6a0f0ef6bc6c616'), (2, 'ca9e985e2e91ca5f83168131fe0b740365266263270fafdaef5321ec6e64c101'), (2, 'e8771cf2e3407f91881badb6f33aefdf58a6b711f76211a90761d1edafd7206a'), (3, '8684d0b554aacdb78b3a2b942a7dab7362025f5e6a78950c51e88ca7d71291f2'), (4, '10c8c518b0adc795a2e1de622545ff79d7a6328e0fa6333990bcf5ae61ca2c58')], 'content/questions.html': [(1, '632d120b6730e0f7745f0a775aa471b7b3fddc6276e7cd121c64c303a4d49d40'), (2, '62f5f0490e482000fb4c21da5ff50166f550b985e575cd6b6522dfc9008938b0'), (2, '95174eee7d69399604ed621cf5901e4c71968567ace4f811735d0d4782650494'), (3, '3d52e64a866c8727643e48e62b4917124fca59474270185afd7b563bf0a3e865')], 'observatory/index.html': [(6, '056188c6569edb785133ac3ef40829afd439deb34d9eca1b4f0086575f60aeec'), (6, '22486f067dc75c138d3309cde861e8f46feb7f089a03c85e39d855227b337642'), (6, '38136ec7e019171d9e2156da80589d2e039a20194137b1d90c7baca6b18c5d98')], 'case-file/brumadinho.html': [(2, 'dede464cf6f0fb048b1c009fa69bf1d2a2b9553a8ea6089d11989008b4c322f9'), (3, 'd096fabbad18ae417b3bd8dfc210ebc46b80d05dc4ee991f669f413e3688d42d'), (4, '4b1a387d1228fb6967ca66d1fa35a60a8334e33ec5b2c3706f6efdc3db5c05dd'), (5, '575d91500d0d7f4b7d1e1fda046640dd376d52d307290bff679ba1aece3749cf')], 'doctrine/pre-threshold-principle.html': [(2, 'ec161747d1ab4a0017ce3c57c374f4ad778ae7193720611827848e84e1b4b108'), (4, '832f57a44e1898a2528b000dcc344ea0af48f7ad50da01604bc06e8fe9a26d1f'), (5, '4db0b2692db3969655c19cde57b0b6c6e94671b61e6723c3e06cbbfff6b9a786'), (6, 'beb12cc41f67340b3f6c2811f18e685cec5df4cc1063d650a99d80b0ee12bb29')], 'index.html': [(2, '0677213da59494679b6d6819bba8e40d19e41114ce04b90f9a836f9dd71105f9'), (2, '3aaffb54fc193d26b23789d4fcc49e4ee01018a77581e052f9749c5ee8aa905a'), (2, '7f2471cec06360055c35c0a4f6aa0d8ce50d8af236a550e1386245dc6ca60a28'), (2, 'a059012c84767fdd104e3dd498caed6c47fb7b5b3d8d5a48c0b55d5f1856f038'), (2, 'a72e815cf958783929c393a8148878690195111e531bf5f0f365403d08105d8b'), (2, 'b8085aee8abd911e32d449c628e73006a6ee8103f9bad361891862bcebfc7de4'), (5, '1a2bf2e1feb79a39faca55a61a2a3759ed0f927408d55faf649370d8ce533741')], 'tfp/tfp-concepts.html': [(2, 'b2c8bbda2d2b5d61ffea96e64a44deeb893dca86fde0baebf5fd5379369f180f'), (3, '709140c03cc032df96ca5160e66b7c3df38c15078815d13e7abaa7bed8f82d7d'), (5, '7bd001ad455ec9a0bb3a9a25752a433b589ea1ccaec09a982c6943d1a14049ea')], 'pt/ptp.html': [(6, 'b22cc34a9e7839e05af0bbb5c2c7c3f45a4ac979232eb4a697f059f1a568d503')], 'pt/observatory/playbooks/index.html': [(2, '99d21959d722aefed608d52b350ba114080bfd52d244d38b618a7a867943fefa'), (3, '21fc5c9acddb9eacad4266d7d616772dc4663066ce7a27fd3ad5cb124702c0c6'), (3, '8c4184a72d81d1de2fe75a66e5c25c23fffac426cfd1d5ede03ec9c7e0094632'), (3, 'e44fdc25827cce16eb15d4b8f332368a246f6d2ba05ea219756fc2f93f24db18')], 'tfp/tfp-intro.html': [(2, '2ef2673f3979156123c51ebe9dfe5a7559286e7259ea8262e1fcce656cbb461d'), (3, '15727a3a9a4e9f6d2eaddf386fef69b614dc2a47188bf9481a876ce8fc9c3bc9'), (3, 'e7b28e4ad39bb98fdf7f66231905abcc80fa2356dcb358254f9951b192ff4477'), (4, 'bf90140ed87f199a914f4856f456cab4e8d0e19eca19f73ef9b4b1cd2e3fa2b3'), (4, 'f0c40c0f037cc226fce717ed04d28f53d30f6f83a4a46a0623ef4dbdfe3e56f4'), (6, '86dbc60da47f7beac701a8b8ba4d23345b1f896be5b3d8c5685cb8d50a32f673')], 'analysis/brum.html': [(2, 'd0b29ffd2c3071c299d4a16026e7867af1ec6aa9192e4b629917f4bdb28b268e'), (3, '516f56efa5bba9f3404118d03bd3abd45e49d6e63877217533cce8036c06fcdb'), (3, '8ab1c16e312757bca7129fd20bb4b3cb1bb0572b13458fcff7f7911bc0d16fb3'), (4, '6917e16ea50949406c1994dd839d8d926439858d2b0d59fe2f036dc47cd42153')], 'observatory/publications/from-orbit-to-the-high-seas.html': [(3, '7e20e370c4251b35b6ea4fdeb267c97c0b413513e40425c2419650c7219dcec8'), (4, '51ad40bd05124afb1b73f5bb9ed881c6be3e2a2fbd44bea3833f43f421800a41'), (5, '087ba86daa30bde792913899665b80bc1d6e69bf432dbd0e6d8ee462d57682bc')], 'pt/applied-study.html': [(3, '7deee448349838f49d1824b441b9b8c2e79f80761dd95d470cea0f8f68dbc3ae'), (3, '9f0556db21ab9d9047c40a23e6c999885646c7099f0e37db8ba2b9c40d9fec4c'), (3, 'd84e45837aaa140ce2caa4352b6afdb5077a0bb460dfe65f0ec88e910a0fe1a8'), (6, '6a4370e63074abf3a86652b9a632a8b7df15f3c88dd870b804794b6b5faeccfe')], 'pt/observatory/publications/from-orbit-to-the-high-seas.html': [(6, '7c71457d1d973914442627ea3abbaff7f0d896185252625998866119e64bf723')], 'enterprise/feasibility.html': [(2, '781972886a214d755024007ae5672b11d25af1b4c377bcfc34793adfab69558d'), (5, '55dd96c3990144ca9d8fcb552dc92b1a7123889dcded628ec3080e5805fb301c'), (7, '61ee3bfffdf29c3c85f1d815c3c1444d828b7eba317fdb746fbe77be4ff48a39')], 'field-notes/index.html': [(3, '33bbb626c96595cb524e2cf8063ffba64de878211ab88b6edd47af3d74848acd'), (3, '7b136c2a5cbe130ebb6f872e39d68dd6e8c252df53a1ea8fe9a8e7a88122d2f6'), (3, 'b68e4eccabbdcf1f3aa2648ea08c8687dc62f900f04609307abd5c0d07746f98')], 'sectors/prudential-risk.html': [(2, 'ca9240a0d282c07297839e4f5e0fa0e204e1398cba0fbd8c7c2222b01c3b7eb7'), (6, 'ed3af35c6ed9888c2498383176b611a401b74b36c32a596e930fe629b715adf8')], 'sectors/gsm-ai.html': [(2, '383696b1128c654d48259607e1cc60ae5c4fe80f76fcadd445b56214bbf2b673'), (2, '56e4cd340a7fbf6a546d0c3cc333d23cae48d6b525202daf1e9c43ee53fb6a5a'), (2, 'bee98faafd34bf34edd6aa56b3af1b8b50498f4d9224938f6943e7d879988ad6')], 'sectors/gsm-es.html': [(2, '383696b1128c654d48259607e1cc60ae5c4fe80f76fcadd445b56214bbf2b673'), (2, '56e4cd340a7fbf6a546d0c3cc333d23cae48d6b525202daf1e9c43ee53fb6a5a'), (2, 'bee98faafd34bf34edd6aa56b3af1b8b50498f4d9224938f6943e7d879988ad6')], 'sectors/gsm-watersys.html': [(2, '383696b1128c654d48259607e1cc60ae5c4fe80f76fcadd445b56214bbf2b673'), (2, '56e4cd340a7fbf6a546d0c3cc333d23cae48d6b525202daf1e9c43ee53fb6a5a'), (2, 'bee98faafd34bf34edd6aa56b3af1b8b50498f4d9224938f6943e7d879988ad6')], 'sectors/gsm-solargeo.html': [(2, '383696b1128c654d48259607e1cc60ae5c4fe80f76fcadd445b56214bbf2b673'), (2, '56e4cd340a7fbf6a546d0c3cc333d23cae48d6b525202daf1e9c43ee53fb6a5a'), (2, 'bee98faafd34bf34edd6aa56b3af1b8b50498f4d9224938f6943e7d879988ad6')], 'license.html': [(2, 'ce8fb37d4e971b1538503a2ac6e737f757b237d767cfb2227f4fac821efc899e'), (3, '5119005b78a8979885e00c4c2aa4c17613cc6bb5a7b25c0bb75ae6f2f30bc349'), (4, '88fb217b24349cbf56ad919cdb38e53cdf6bc3f7ed0f57fa0fe7a6d4f116c064')], 'pt/license.html': [(3, '0ee3c33df0f6b14300a82d25344eba06a3a90cb5e5b6cdc1959f573a29720113'), (3, '9f0556db21ab9d9047c40a23e6c999885646c7099f0e37db8ba2b9c40d9fec4c'), (6, '6a4370e63074abf3a86652b9a632a8b7df15f3c88dd870b804794b6b5faeccfe')], 'pt/policy-brief.html': [(1, '0bcb90ef95b70d038aeeb94393486f6877eb66bc366ed8f11653a7544a8107a1'), (3, '9f0556db21ab9d9047c40a23e6c999885646c7099f0e37db8ba2b9c40d9fec4c'), (6, '6a4370e63074abf3a86652b9a632a8b7df15f3c88dd870b804794b6b5faeccfe')], 'content/article01.html': [(2, '2de9b89d8ef44d684d7593e6e611c42890220de5c0c4a5de5f77c7da3bfb0c8f'), (2, '8555acb7b92dff2ab7eee9d12b75c96edc794dbd14ea571e5b543d9aad635dde'), (3, '397b4a4c22be9964e1167746a73876088c897d99f909155e366d960cecfae379'), (4, 'ca26ac967d18a392f4e56b2853215d653a32633aaeb785bbca081d55b49d3ae7')], 'pt/artigo01.html': [(2, 'dbb48a95fd169f118cff16af999cf98d31cb70b13b9e61def2aee26b83d23569'), (2, 'ea2ae8585ea4186d8123ac027dc4d0b1e5bd11eb33577001cfac6788b91d137a'), (3, '2e9055a183dbf2631367c2e102c2147efce2e0808b1017c7d8bb40cab540f848'), (4, '5fa5b1496202189c4b7e5999497684cb14eeee294faf12d3d75e947ef8d76987')], 'pt/portuguese.html': [(2, '441103d2a64b3c9eecdabb921632ba94fa353eb99f088bee7b73d280cb890957'), (4, '0957d436492eb3c6721f27aea82b340f6e525093df8295549e99609d904bd9ec'), (4, 'b8a6fdb6a5b100e5077ecfb5302139747d207a27988619f825cd407aa7c3a503')], 'observatory/case-studies/case-03-ma-transnacional.html': [(2, '2b93e9389495f62131cb12c34351e9f2a3dafaba0c1da5c116ea11c9b883bfbb'), (2, 'c930b267cf63581708ea6e0388bfc3211f8287193abbca725e1ea7368f5ee210'), (3, 'f00a8db09c12e362c0ed1682d6b9948c04e1b4c7aeb19a748d7a6f9e94dd6936')], 'pt/observatory/case-studies/case-03-ma-transnacional.html': [(2, 'f2cce6882b670e9ecd2ce31beef5c729f24119e0d31ec4a4569f136564ce342d'), (3, '005357a896234a0faabd99405f32eb0b712c54b77ed3c0b293036e902ec0f255'), (3, '4e8e0258f5216c8386542be5695e0bdb2187384ed564cdbd15c00beffd8efd00')], 'observatory/case-studies/case-04-supply-chain-ai.html': [(2, '2b93e9389495f62131cb12c34351e9f2a3dafaba0c1da5c116ea11c9b883bfbb'), (2, 'c930b267cf63581708ea6e0388bfc3211f8287193abbca725e1ea7368f5ee210'), (3, 'f00a8db09c12e362c0ed1682d6b9948c04e1b4c7aeb19a748d7a6f9e94dd6936')], 'pt/observatory/case-studies/case-04-supply-chain-ai.html': [(2, 'f2cce6882b670e9ecd2ce31beef5c729f24119e0d31ec4a4569f136564ce342d'), (3, '005357a896234a0faabd99405f32eb0b712c54b77ed3c0b293036e902ec0f255'), (3, '4e8e0258f5216c8386542be5695e0bdb2187384ed564cdbd15c00beffd8efd00')], 'pt/observatory/case-studies/case-02-niobio-amazonia.htm': [(2, 'f2cce6882b670e9ecd2ce31beef5c729f24119e0d31ec4a4569f136564ce342d'), (3, '005357a896234a0faabd99405f32eb0b712c54b77ed3c0b293036e902ec0f255'), (3, '4e8e0258f5216c8386542be5695e0bdb2187384ed564cdbd15c00beffd8efd00')], 'pt/info.html': [(2, '7bf5c3d0a610d4d5074657f370e564fc5fcd0e1bd6311b589253a87b248dfad6'), (3, '0788d9a6dd6578caa80ec043a096a7f8e055b3565e2a22782419753234655b5c')], 'pt/partnerships.html': [(2, '7bf5c3d0a610d4d5074657f370e564fc5fcd0e1bd6311b589253a87b248dfad6'), (3, '0788d9a6dd6578caa80ec043a096a7f8e055b3565e2a22782419753234655b5c')], 'observatory/playbooks/index.html': [(6, '5dc75f80c0cfa76efaa016c4bf7565efd663bfbecc2d25ee8626ee01fd196599')]}
SENSITIVE_OPERATIONAL_PATHS = set(HASH_SIGNATURES_BY_PATH)
RETENTION_MARKERS = re.compile(
    r"not included|not published|withheld|under publication review|não (?:estão|são) incluíd|não (?:está|é) publicad|omitid",
    re.I,
)
GENERIC_FORBIDDEN = {
    "probabilistic_simulation": re.compile(r"Monte\s*Carlo", re.I),
    "formula_assignment": re.compile(r"(?:Γ|Gamma)\s*=\s*[A-Za-z]\s*\(", re.I),
    "numeric_score": re.compile(r"\b(?:score|index|metric)\b[^<\n]{0,70}(?:\d{1,3}\s*[–-]\s*\d{1,3}|\d{1,3}\s*/\s*100)", re.I),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "hardcoded_access_code": re.compile(r"(?:const|let|var)\s+[A-Z_]*CODE\s*=\s*[\"'][^\"']+[\"']", re.I),
}
GENERIC_SENSITIVE = {
    "commercial_amount": re.compile(r"(?:USD|EUR|GBP|R\$|[$€£])\s*\d", re.I),
    "operational_percentage": re.compile(r"\b(?:weight|complexity|selection|funding|allocation)\b[^.\n]{0,80}\d+(?:[.,]\d+)?\s*%", re.I),
    "numbered_layer": re.compile(r"\b(?:TDR\s+)?Layer\s+\d+\b|\bL\d+\s*[–-]\s*L\d+\b", re.I),
    "operational_artifact": re.compile(r"\b(?:operational\s+manual|negotiation\s+playbook|trigger\s+catalogue|risk\s+scoring\s+specification|model\s+clauses\s+pack|board\s+resolution)\b", re.I),
}
MODEL_LAW_PATHS = {
    "doctrine/model-law.html",
    "doctrine/law.html",
    "doctrine/lei-modal.html",
}


def visible_claim_text(text: str) -> str:
    stripped = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", text, flags=re.I | re.S)
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    stripped = re.sub(r"\s+", " ", stripped)
    sentences = re.split(r"(?<=[.!?])\s+", stripped)
    return " ".join(sentence for sentence in sentences if not RETENTION_MARKERS.search(sentence))


def token_hashes(text: str, sizes: set[int]) -> set[tuple[int, str]]:
    import hashlib
    import html as html_module

    plain = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", text, flags=re.I | re.S)
    plain = re.sub(r"<[^>]+>", " ", plain)
    tokens = re.findall(r"[^\W_]+", html_module.unescape(plain).lower(), re.UNICODE)
    found: set[tuple[int, str]] = set()
    for size in sizes:
        if size <= 0 or size > len(tokens):
            continue
        for index in range(len(tokens) - size + 1):
            digest = hashlib.sha256(" ".join(tokens[index:index + size]).encode("utf-8")).hexdigest()
            found.add((size, digest))
    return found


def public_files() -> list[Path]:
    paths: list[Path] = []
    for current, directories, filenames in os.walk(ROOT):
        directories[:] = [
            name for name in directories if name not in {".git", ".hermes", "__pycache__"}
        ]
        paths.extend(Path(current) / name for name in filenames)
    return paths


class RefCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.refs.extend(value for key, value in attrs if key.lower() in LINK_ATTRS and value)

    handle_startendtag = handle_starttag


def candidates(source: Path, raw: str) -> list[Path]:
    value = raw.strip()
    if not value or value.startswith(IGNORED_PREFIXES):
        return []
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return []
    path = unquote(parsed.path)
    target = ROOT / path.lstrip("/") if path.startswith("/") else source.parent / path
    targets = [target]
    if not target.suffix:
        targets.extend((target.with_suffix(".html"), target / "index.html"))
    return targets


def main() -> int:
    errors: list[str] = []
    files = public_files()
    html_files = sorted(path for path in files if path.suffix.lower() in {".html", ".htm"})
    reference_count = 0

    for source in html_files:
        text = source.read_text(encoding="utf-8", errors="replace")
        parser = RefCollector()
        try:
            parser.feed(text)
            parser.close()
        except Exception as exc:
            errors.append(f"HTML parse error: {source.relative_to(ROOT)}: {exc}")
            continue
        reference_count += len(parser.refs)
        for raw in parser.refs:
            targets = candidates(source, raw)
            if targets and not any(target.exists() for target in targets):
                errors.append(f"Missing internal reference: {source.relative_to(ROOT)} -> {raw}")

    for relative in REMOVED_PATHS:
        if (ROOT / relative).exists():
            errors.append(f"Removed technical artifact is present: {relative}")

    for relative in SUSPENDED_PATHS:
        path = ROOT / relative
        if not path.exists() or "Temporarily unavailable" not in path.read_text(
            encoding="utf-8", errors="replace"
        ):
            errors.append(f"Suspension notice missing: {relative}")

    model_law = ROOT / "doctrine/model-law.html"
    if not model_law.exists() or "Model Law" not in model_law.read_text(
        encoding="utf-8", errors="replace"
    ):
        errors.append("Canonical Model Law is missing")

    searchable_suffixes = {".html", ".htm", ".js", ".ts", ".tsx", ".md", ".json"}
    global_sizes = {size for size, _digest in HASH_SIGNATURES_GLOBAL}
    for path in sorted(path for path in files if path.suffix.lower() in searchable_suffixes):
        relative = path.relative_to(ROOT).as_posix()
        if relative in MODEL_LAW_PATHS or relative == "scripts/verify_static.py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        claims = visible_claim_text(text)
        for name, pattern in GENERIC_FORBIDDEN.items():
            if pattern.search(claims):
                errors.append(f"Forbidden public signal ({name}): {relative}")
        path_signatures = HASH_SIGNATURES_BY_PATH.get(relative, [])
        wanted = set(HASH_SIGNATURES_GLOBAL) | set(path_signatures)
        sizes = global_sizes | {size for size, _digest in path_signatures}
        if wanted and token_hashes(claims, sizes) & wanted:
            errors.append(f"Forbidden hashed public signature: {relative}")
        if relative in SENSITIVE_OPERATIONAL_PATHS:
            for name, pattern in GENERIC_SENSITIVE.items():
                if name == "commercial_amount" and relative in {"enterprise/alpha.html", "fellowship/cases/fellowship-cs-brumadinho.html"}:
                    continue
                if pattern.search(claims):
                    errors.append(f"Forbidden operational signal ({name}): {relative}")

    result = {
        "ok": not errors,
        "html_files": len(html_files),
        "references": reference_count,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
