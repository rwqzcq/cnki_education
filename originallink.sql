/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50505
 Source Host           : localhost
 Source Database       : education_journal

 Target Server Type    : MySQL
 Target Server Version : 50505
 File Encoding         : utf-8

 Date: 05/15/2019 16:08:09 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `originallink`
-- ----------------------------
DROP TABLE IF EXISTS `originallink`;
CREATE TABLE `originallink` (
  `ID` varchar(100) NOT NULL,
  `TITLE` varchar(2000) NOT NULL DEFAULT '' COMMENT '标题',
  `SHORT_DESC` varchar(4000) DEFAULT NULL COMMENT '短描述',
  `THUMBNAIL` varchar(4000) DEFAULT NULL COMMENT '缩略图',
  `CONTENT` longtext COMMENT '正文',
  `RELEASE_DATETIME` varchar(100) DEFAULT NULL COMMENT '发稿/发布时间',
  `RELEASE_DATETIME_END` varchar(100) DEFAULT NULL COMMENT '结束时间。会议用',
  `SOURCE` varchar(100) DEFAULT NULL COMMENT '信息来源',
  `SOURCE_REAL` varchar(100) DEFAULT NULL COMMENT '真实来源',
  `SOURCE_MENU_LV1` varchar(100) DEFAULT NULL COMMENT '信息来源-1级栏目',
  `SOURCE_MENU_LV2` varchar(100) DEFAULT NULL COMMENT '信息来源-2级栏目',
  `MEDIA_TYPE` varchar(100) DEFAULT NULL COMMENT '媒介类型:新闻，会议，政策',
  `YEAR_AND_VOLUME_OR_PERIOD` varchar(100) DEFAULT NULL COMMENT '年卷（期）',
  `DOI` varchar(100) DEFAULT NULL COMMENT '数字对象唯一标识符',
  `ISSN` varchar(100) DEFAULT NULL COMMENT '国际刊号',
  `JOURNAL_FULL_DESC` varchar(200) DEFAULT NULL COMMENT '期刊完整描述',
  `AUTHOR` varchar(200) DEFAULT NULL COMMENT '作者(多个)',
  `EDITOR` varchar(100) DEFAULT NULL COMMENT '编辑',
  `AUDITOR` varchar(100) DEFAULT NULL COMMENT '审核人',
  `PHOTOGRAPHY` varchar(100) DEFAULT NULL COMMENT '摄影',
  `CORRESPONDENT` varchar(50) DEFAULT NULL COMMENT '通讯员',
  `WORDS` varchar(200) DEFAULT NULL COMMENT '文',
  `PICTURE` varchar(200) DEFAULT NULL COMMENT '图',
  `ORIGINAL_PUBLISHER` varchar(200) DEFAULT NULL COMMENT '原文刊载于',
  `ORIGINAL_LINK_LV1` varchar(1000) DEFAULT NULL COMMENT '栏目地址，工具用',
  `ORIGINAL_LINK` varchar(2000) DEFAULT NULL COMMENT '原文链接',
  `ORIGINAL_URL` varchar(200) DEFAULT NULL COMMENT '原文链接，工具用',
  `REPRINT_STATEMENT` varchar(50) DEFAULT NULL COMMENT '转载声明',
  `SPECIAL_THANKS` varchar(200) DEFAULT NULL COMMENT '特别鸣谢',
  `HITS` int(50) DEFAULT NULL COMMENT '访问/浏览次数',
  `TAGS` text COMMENT '标签',
  `SUBJECT_TYPE` varchar(200) DEFAULT NULL COMMENT '学科分类',
  `CONTENT_TYPE` varchar(200) DEFAULT '' COMMENT '内容分类',
  `HASH_CODE` varchar(50) DEFAULT NULL COMMENT ' 所有字段值相加生成一个唯一的标识',
  `HASH_CODE_COPY` varchar(50) DEFAULT NULL COMMENT '替换图片文本之前的HASH_CODE',
  `IS_NEWS` int(11) DEFAULT '0' COMMENT '是否已经导入新闻列表',
  `SCRIPT_DELETE` int(2) DEFAULT NULL,
  `BZY_SCRIPT_VERSION` varchar(100) DEFAULT NULL COMMENT '八爪鱼脚本版本号',
  `ADD_USERID` varchar(32) DEFAULT NULL COMMENT '添加用户ID',
  `ADD_TIME` datetime DEFAULT NULL COMMENT '添加人时间',
  `ADD_NAME` varchar(30) DEFAULT NULL COMMENT '添加人姓名',
  `UPD_USERID` varchar(32) DEFAULT NULL COMMENT '修改人ID',
  `UPD_TIME` datetime DEFAULT NULL COMMENT '修改时间',
  `UPD_NAME` varchar(30) DEFAULT NULL COMMENT '修改人姓名',
  `U_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '时间戳',
  `U_DELETE` int(2) DEFAULT '1',
  `NEWS_PICTURES` varchar(1000) DEFAULT NULL COMMENT '新闻图片路径',
  `SEARCH_WORDS_ID` varchar(32) DEFAULT NULL COMMENT '源搜索词',
  `SEARCH_WORDS_NAME` varchar(200) DEFAULT NULL COMMENT '源搜索词',
  `ORIGIN_STATE` varchar(32) DEFAULT 'PENDING' COMMENT '状态 待分配、已分配、已推送、审核不通过',
  `ASSIGN_USER_ID` varchar(32) DEFAULT NULL COMMENT '分配人',
  `ASSIGN_USER_NAME` varchar(50) DEFAULT NULL COMMENT '分配人',
  `ASSIGN_DATE` datetime DEFAULT NULL COMMENT '分配时间',
  `AUDIT_REASON` varchar(500) DEFAULT NULL COMMENT '审核不通过原因',
  `NEWS_PICTURES_COPY` varchar(1000) DEFAULT NULL COMMENT '微信图片地址复制',
  `QUALITY_LEVEL` varchar(100) DEFAULT 'UNCATEGORIZED' COMMENT '质量等级',
  `WX_URL_REPLACE` varchar(10) DEFAULT NULL COMMENT '微信地直是否替换',
  PRIMARY KEY (`ID`) USING BTREE,
  KEY `originalink_TITLE` (`TITLE`(255)) USING BTREE,
  KEY `originalink_HASH_CODE` (`HASH_CODE`) USING BTREE,
  KEY `originalink_ADD_TIME` (`ADD_TIME`) USING BTREE,
  KEY `originalink_QUALITY_LEVEL` (`QUALITY_LEVEL`) USING BTREE,
  KEY `originalink_SOURCE` (`SOURCE`,`SOURCE_REAL`) USING BTREE,
  KEY `originalink_WX_URL_REPLACE` (`WX_URL_REPLACE`) USING BTREE,
  KEY `originalink_SOURCE_REAL` (`SOURCE_REAL`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
